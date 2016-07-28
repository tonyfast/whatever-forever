
# coding: utf-8

# In[1]:

import builtins
import toolz.curried
from toolz.curried import *
from types import MethodType
from typing import Callable
from copy import deepcopy


# In[2]:

"""Compose a function by chaining.

Chain([1,2,]).map(lambda x: x*2).list().value()

"""
class Chain(object):
    _imports = [
        builtins,
        toolz.curried,
    ]
    
    def __init__(
        self,
        context=None,
        imports=[],
        eager = True,
    ):
        """Initialize the Chain method.  Include a context to evaluate the function one.
        """
        self._imports.extend(imports)
        pipe(
            self._imports, dir, concat, unique, filter(
                complement(lambda x: x[0] != '_')
            ), map(
                lambda x: setattr(self, x, self._getter)
            ), list
        )
        self._context = context
        self._tokens = [[identity, [], {}]]
        self.eager = eager


# In[3]:

new_method = lambda x: setattr(Chain, x.__name__, x)


# In[4]:

@new_method
def _compose(self):
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


# In[5]:

@new_method
def value(self, *args, **kwargs):
    fn = self._compose()
    if args or kwargs:
        return fn(*args, **kwargs)
    return fn(self._context)


# In[6]:

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


# > Get a callable with a string alias.  last package with 
# the attribute
# 
# ```python
# Chain()._getter('map')
# ```

# In[7]:

@new_method
def __getattr__(self, attr):
    self._tokens.append([self._getter(attr), [], {}])
    return self


# > Chain callables as attributes of the chain.
# 
# ```python
# Chain().map.partition.concat
# ```

# In[8]:

@new_method
def __getitem__(self, item):
    self._tokens.append([item, (), {}])
    return self


# > Add any function to the chain.  This function doesn't have to be in 
# `self.imports`
# 
# ```python
# Chain().__getitem__('map')
# ```

# In[9]:

@new_method
def __call__(self, *args, **kwargs):
    self._tokens[-1][1] = args
    self._tokens[-1][2] = kwargs
    return self


# > include arguments for the last token that was created.
# 
# ```python
# Chain().map(lambda x: x*2)
# ```

# In[10]:

@new_method
def __repr__(self):
    if not isinstance(self._context, type(None)) and self.eager:
        return self.value().__str__()
    return self._tokens.__str__()


# In[11]:

@new_method
def copy(self):
    chain = Chain(self._context)
    chain._imports = self._imports[:]
    chain._tokens = self._tokens[:]
    return chain   


# In[12]:

@new_method
def __or__(self, f):
    chain = self.copy()
    chain._tokens.append([f, [], {}])
    return chain


# ```python
# v = Chain([1,2]) | map(lambda x: x**2) | list
# assert type(v) == Chain
# ```

# In[13]:

@new_method
def __gt__(self, f):
    return self.copy()[f].value()


# ```python
# Chain([1,2]).map(lambda x: x**2) > list
# ```
