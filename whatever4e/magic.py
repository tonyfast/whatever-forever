
# coding: utf-8

# In[17]:

from class_maker import method
from IPython import display, get_ipython
from IPython.core import magic_arguments
from IPython.core.magic import (
    Magics,
    magics_class,
    line_cell_magic,
)
from toolz.curried import *


# In[18]:

@magics_class
class Whatever(Magics):
    def __init__(self, name, f, magic_kind='cell', lang=None, **kwargs):
        """Initialize a new [cell/line] magic.  The executes f on the [cell/line] body.
        """
        self.name = name
        self.f = f
        if lang:
            pipe("""require([
                        "notebook/js/codecell",
                        "codemirror/mode/{0}/{0}"
                    ],
                    function(cc){{
                        cc.CodeCell.options_default.highlight_modes.magic_{1} = {{
                            reg: ["^%%{1}"]
                        }};
                    }}
                );
                """.format(lang, name), 
                 display.Javascript, display.display,
            )
        get_ipython().register_magic_function(
            partial(self.forever, f=f, **kwargs),
            magic_kind=magic_kind, magic_name=name,
        )
        


# In[19]:

new_method = add_method(Whatever)


# In[20]:

@new_method
@line_cell_magic
@magic_arguments.magic_arguments()
@magic_arguments.argument(
    "name",
    default=None,
    nargs="?",
    help="""Name of local variable to set to parsed value""",
)
@magic_arguments.argument(
    "-c",
    "--code",
    default="",
    help="""Some code to run.""",
)
@magic_arguments.argument(
    "-d",
    "--display",
    default=-1,
    nargs="?",
    help="""An IPython.display method."""
)
def forever(cls, line, cell="""""", f=identity, display=None):
    args = magic_arguments.parse_argstring(cls.forever, line.strip())
    if not cell:
        cell = pipe(args.code, lambda x: eval(x, get_ipython().user_ns))
    
    if args.display != -1:
        display = args.display
    
    val = f(cell)
    if bool(args.name):
        get_ipython().user_ns[args.name] = val

    return cls.show(display, val)


# In[21]:

@new_method
def line(cls, name, f, display='HTML', lang=None):
    return partial(cls, name, magic_kind='line', display=display, lang=lang)(f)        


# In[22]:

@new_method
def cell(cls, name, f, display='Markdown', lang=None):
    return partial(cls, name, display=display, lang=lang)(f)


# In[23]:

@new_method
def show(cls, disp, val):
    if disp:
        if isinstance(disp, str):
            return display.display(getattr(display, disp)(val))
        elif isinstance(disp, Callable):
            return display.display(disp(val))


# In[24]:

w = Whatever('test', identity,)


# In[27]:

@staticmethod
@new_method
def test(cls, i=1):
    return i
