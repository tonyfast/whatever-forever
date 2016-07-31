
# coding: utf-8

# It should be easier to construct complicated functions.  Python has named a lot of things, and
# large scale adoption of certain libraries make names meaningful.  `Chain` is inspired by `pytoolz`
# and `underscorejs`.  The `pytoolz` documentation does a fantastic describing functional programming.
# 
# There are a few functional programming tools in Python ecosystem.  I would up breaking them 
# very quickly after trying them __Or__ the didn't work in the Jupyter notebook.
# 
# A `Chain` is efficient for prototyping and scaling complicated actions.  
# 
# A Chain class
# 
# * composes functions.  `Chain` must be explicitly computed using `value` or `>`
# * has a special attribute `value`
# * overloads `__or__` and `__gt__`
#     * Provides semi-functional syntax for evaluation

# The only required import is `toolz` from pypi

# In[89]:

from .class_maker import method
import builtins
import toolz.curried
from toolz.curried import *
from types import MethodType
from typing import Callable


# In[62]:

"""Compose a function by chaining.

Chain([1,2,]).map(lambda x: x*2).list().value()

"""
class Chain(object):
    _imports = [
        builtins,
        toolz.curried,
    ]


# In[90]:

new_method = method(Chain)


# In[91]:

@new_method
def _getter(self, key):
    """
    """
    return pipe(
        self._imports,
        reversed, 
        map(
            lambda imp: getattr(imp, key) if hasattr(imp, key) else None,
        ),
        filter(bool),
        first, 
    )


# In[92]:

@new_method
def __init__(
    self,
    *args, **kwargs
):
    """Initialize the Chain method.  Include a context to evaluate the function one.
    """
    pipe(
        self._imports, dir, concat, unique, filter(
            complement(lambda x: x[0] != '_')
        ), map(
            lambda x: setattr(self, x, self._getter)
        ), list
    )
    self._tokens = []
    self._args = args
    self._kwargs = kwargs


# > Method to compose a function from the tokens that 
# have been created in the chain

# In[93]:

@new_method
def _compose(self):
    return compose(
        *pipe(
            self._tokens if self._tokens else [[identity, [], {}]],
            reversed,
            map(
                lambda e: partial(
                    e[0], *e[1], **e[2]
                ) if e[1] or e[2] else e[0],
            )
        ),
    )


# > `value` composes the function and then evaluate it with either 
# the default context or a new set of arguments to evaluate with the same composition.

# In[94]:

@new_method
def value(self, *args, **kwargs):
    fn = self._compose()
    if args or kwargs:
        return fn(*args, **kwargs)
    if self._kwargs: 
        return fn(*self._args, **self._kwargs)
    return fn(*self._args)


# > Get a callable with a string alias.  last package with 
# the attribute
# 
# ```python
# Chain()._getter('map')
# ```

# > Bah, the attribute is just a string.  What function does that refer to in the imports?

# In[95]:

@new_method
def __getattr__(self, attr):
    self._tokens.append([self._getter(attr), [], {}])
    return self


# > A mighty flexible way to append any function the chain.

# In[96]:

@new_method
def __getitem__(self, item):
    self._tokens.append([item, (), {}])
    return self


# > `__call__` does not execute anything it just records args 
# and kwargs that would be passed to the function.

# In[97]:

@new_method
def __call__(self, *args, **kwargs):
    self._tokens[-1][1] = args
    self._tokens[-1][2] = kwargs
    return self


# > A `Chain` is a `Chain` until `value` or `|`.  
# 
# > If a `Chain` is printed, and it is `eager` (by default) then the composition
# will be executed if there is a context.

# In[98]:

@new_method
def __repr__(self):
    return self.value().__str__()


# > Copy the state of the chain and return a new one.

# In[99]:

@new_method
def copy(self):
    chain = Chain(*self._args, **self._kwargs)
    chain._imports = self._imports[:]
    chain._tokens = self._tokens[:]
    return chain   


# > Some sweet ol' syntactic sugar that looks like functional programming.
# 
# > `__or__` adds a piping method to a chain.  Any functional can be included in the pipe.
# 
# > `__or__` is shorthand for a copy and a an append.

# In[100]:

@new_method
def __or__(self, f):
    chain = self.copy()
    chain._tokens.append([f, [], {}])
    return chain


# > `__gt__` is shorthand for a copy, append, and a `value` operation.

# In[101]:

@new_method
def __gt__(self, f):
    return self.copy()[f].value()


# In[ ]:



