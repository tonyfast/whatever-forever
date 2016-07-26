
# coding: utf-8

# In[10]:

from IPython import display, get_ipython
from IPython.core import magic_arguments
from IPython.core.magic import (
    Magics,
    magics_class,
    line_cell_magic,
)
import builtins
import toolz.curried
from toolz.curried import *
from typing import Callable

__version_info__ = (0, 2, 0)
__version__ = '.'.join(map(str, __version_info__))


__all__ = [
    'Whatever', 'Chain',
]


# # Designing Interactive Data Applications in the Notebook
# 
# The Jupyter notebook is a robust tool that can combine the power of Python with the versatility of Javascript.
# 
# 
# ![](https://qph.ec.quoracdn.net/main-qimg-8d0d7c58813161115fc9adc1037efa87-c?convert_to_webp=true)
# 
# This comic would be funny if it were true.  Python is so easy to get started; then the lines start to stack up.  When does our toy code transition to real code?  Idea code vs. Usable code?

# # `Whatever` class
# 
# > Separate your model from presentation.
# 
# Turn whatever you want into a reusable a tool.
# 
# ## BoilerPlate
# 

# In[7]:

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
        
    @classmethod
    def line(cls, name, f, display='HTML'):
        return partial(cls, name, magic_kind='line', display=display)(f)
        
    @classmethod
    @curry
    def cell(cls, name, f, **kwargs):
        return partial(cls, name, **kwargs)(f)
    
    @classmethod
    def display(cls, disp, val):
        if disp:
            if isinstance(disp, str):
                return display.display(getattr(display, disp)(val))
            elif isinstance(disp, Callable):
                return display.display(disp(val))

    
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


# # It's sucks to run out of paper!
# 
# Remember when you used to really write in a notebook?  You were doing your homework.  Just finishing a problem.   
# Oh No!  You're close to the edge!  Start smooshing the letters!  Oops, you ran out of paper!  Yea, that feeling sucked!
# 
# It is really nice to keep a problem in scope.  The more you can see, the more you explore.  `Chain` applies the
# [underscorejs `chain` syntax](http://underscorejs.org/#chaining) to `builtins` and `pytoolz.curried`.  `Chain` saves
# space and it is great for functional programming.

# In[8]:

"""Compose a function by chaining.

Chain([1,2,]).map(lambda x: x*2).list().value()

"""
class Chain(object):
    _imports = [
        builtins,
        toolz.curried,
    ]
    
    def _getter(self, key):
        return pipe(
            self._imports,
            reversed, 
            map(
                lambda imp: getattr(imp, key) if hasattr(imp, key) else None,
            ),
            filter(bool),
            first, 
        )
    
    def __init__(
        self,
        context=None,
        imports=[],
    ):
        """Initialize the Chain method.  Include a context to evaluate the function one.
        """
        self.context = context
        self._imports.extend(imports)
        self._tokens = []
        
    def __getitem__(self, item):
        self._tokens.append([item, (), {}])
        return self
    
    def __getattr__(self, attr):
        self._tokens.append([self._getter(attr), [], {}])
        return self
    
    def __call__(self, *args, **kwargs):
        self._tokens[-1][1] = args
        self._tokens[-1][2] = kwargs
        return self
    
    @property
    def f(self):
        return compose(
            *pipe(
                self._tokens,
                reversed,
                map(
                    lambda e: partial(
                        e[0], *e[1], **e[2]
                    ) if e[1] or e[2] else e[0],
                )
            ),
        )
            
    def value(self, *args, **kwargs):
        if args or kwargs:
            return self.f(*args, **kwargs)
        return self.f(self.context)

