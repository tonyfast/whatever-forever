
# coding: utf-8

# # `whatever-forever`
# 
# For developing dense ideas in the notebook.
# 
# * Easy to define cell magics.
# * Syntatic sugar for composing and evaluating complex functional operations.
# 
# `pip install whatever-forever`

# ## `Chain`
# 
# A chain is a typographically compact manner of creating complicated
# expressions in Pythonic syntax.
# 
# ### Chainable Values
# 
# ```python
# from whatever import *
# some_expr = Chain([1,2,3]).reversed().map(lambda x: x**2).list()
# some_expr.value()
# some_expr.value([3,5,8])
# ```
# 
# ### Syntactic Sugar
# 
# `_X` provides syntactic sugar for composing expressions.
# 
# ```python
# 
# some_expr = _X([1,2,3]) | reversed | map(lambda x: x**2) | list
# some_value = _X([1,2,3]) | reversed | map(lambda x: x**2) > list
# ```

# ## Development
# 
# Running test and the docs server.
# 
# ```
# watchmedo tricks tricks.yaml
# jekyll serve docs -wit
# ```

# ## `Whatever`
# 
# Easy to construct cell magics
# 
# ### Cell Magics
# 
# Create a `jinja` to Markdown magic.
# 
# ```python
# from jinja2 import Template
# @magical('jinja2', lang='jinja2', display='Markdown')
# def render_jinja_with_globals(cell):
#     return Template(cell).render(**globals())
# ```

# ## License
# `whatever-forever` is released as free software under the [BSD 3-Clause license](https://github.com/tonyfast/whatever-forever/blob/master/LICENSE).

# In[ ]:

__version_info__ = (0, 0, 12)
__version__ = '.'.join(map(str, __version_info__))

from .chain import Chain, this, _X
from .magic import magical
from .class_maker import method
from toolz.curried import *
import toolz.curried

__all__ = [
    'magical', 'Chain', 'method', 'this', '_X', *pipe(
        toolz.curried, dir, filter(
            complement(lambda s: s.startswith('_'))
        ), list
    )
]

