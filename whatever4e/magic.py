
# coding: utf-8

# In[2]:

from IPython import display, get_ipython
from IPython.core import magic_arguments
from IPython.core.magic import (
    Magics,
    magics_class,
    line_cell_magic,
)
from typing import Callable
from toolz.curried import *


# > Evaluate arbitrary variables that can be added to the global context by defining a name.

# In[21]:

@magic_arguments.magic_arguments()
@magic_arguments.argument(
    "name",
    default=None,
    nargs="?",
    help="""Name of local variable to set to parsed value""",
)
@magic_arguments.argument(
    "-d",
    "--display",
    default='Markdown',
    nargs="?",
    help="""An IPython.display method."""
)
def magical_cell(line, cell, f=identity, **kwargs):
    args = magic_arguments.parse_argstring(magical_cell, line.strip())

    retval = f(cell)
    
    if args.name:
        if '.' in args.name:
            path = args.name.split('.')
            var = get_ipython().user_ns[path[0]]
            setattr( reduce(
                lambda x, y: getattr(x,y),
                path[1:-1], 
                var
            ), path[-1], retval)
        else:   
            get_ipython().user_ns[args.name] = retval
    
    
    if args.display:
        disp = kwargs['display'] if 'display' in kwargs else args.display
        if isinstance(disp, str):
            return display.display(getattr(display, disp)(retval))
        elif isinstance(disp, Callable):
            return disp(retval)


# In[4]:

class magical():
    def __init__(self, magic_kind=magical_cell):
        self._magic_kind = magic_kind
    
    @curry
    def __call__(self, key, f, lang=None, **kwargs):
        name = self._magic_kind.__name__.split('_')[1]
        get_ipython().register_magic_function(
            partial(self._magic_kind, f=f, **kwargs),
            magic_kind = name,
            magic_name = key,
        )
        if lang:
            # Syntax highlighting
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


# > Still don't know how I will use this.

# In[5]:

def magical_line(line, f=identity, **kwargs):    
    """I don't understand how I would use this yet."""
    if 'assign' in kwargs:
        if kwargs['assign']:
            line, cell = line.strip().split(' ',1)
    else:
        line, cell = ['', line]
    return magical_cell(line, cell, f, **kwargs)


# In[6]:

class Forever(object):
    cell = staticmethod(magical(magical_cell))
    line = staticmethod(magical(magical_line))

