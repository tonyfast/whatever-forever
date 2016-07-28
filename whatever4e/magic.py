
# coding: utf-8

# In[14]:

from IPython import display, get_ipython
from IPython.core import magic_arguments
from IPython.core.magic import (
    Magics,
    magics_class,
    line_cell_magic,
)
from toolz.curried import *


# In[15]:

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
        


# In[16]:

new_method = lambda x: partial(setattr, Whatever, x)


# In[17]:

@new_method('line')
@classmethod
def line(cls, name, f, display='HTML'):
    return partial(cls, name, magic_kind='line', display=display)(f)
        


# In[18]:

@new_method('cell')
@classmethod
@curry
def cell(cls, name, f, **kwargs):
    return partial(cls, name, **kwargs)(f)


# In[19]:

@new_method('display')
@classmethod
def display(cls, disp, val):
    if disp:
        if isinstance(disp, str):
            return display.display(getattr(display, disp)(val))
        elif isinstance(disp, Callable):
            return display.display(disp(val))


# In[20]:

@new_method('forever')
@classmethod
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
    default="Markdown",
    nargs="?",
    help="""An IPython.display method."""
)
def forever(cls, line, cell="""""", f=identity, **kwargs):
    args = magic_arguments.parse_argstring(cls.forever, line.strip())
    if not cell:
        cell = pipe(args.code, lambda x: eval(x, get_ipython().user_ns))

    val = f(cell)

    for key, value in kwargs.items():
        if hasattr(args, key):
            setattr(args, key, value)        

    if bool(args.name):
        get_ipython().user_ns[args.name] = val

    return cls.display(args.display, val)

