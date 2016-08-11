
# coding: utf-8

# It should be easier to construct complicated functions.  Python has named a lot of things, and
# large scale adoption of certain libraries make names meaningful.  `Chain` is inspired by `pytoolz`
# and `underscorejs`.  The [`pytoolz` documentation does a fantastic describing functional programming](toolz.readthedocs.io).
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
# * a `copy` method
# * overloads `__or__` and `__gt__`
#     * Provides semi-functional syntax for evaluation

# The only required import is `toolz` from pypi

# In[5]:

from .class_maker import method
import builtins
import operator
import toolz.curried
from toolz.curried import *
from types import MethodType
from typing import Callable


# In[6]:

class Chain(object): 
    _imports = [toolz.curried, operator, builtins]
    
new_method = method(Chain)


# In[7]:

@new_method
def __init__(
    self,
    *args, **kwargs
):
    # A function to extract attributes from a module.
    module_methods = lambda module: pipe(module, dir, filter(
            lambda x: not x.startswith('_')
        ), map(
            partial(getattr, module)
        ), list)
    
    # Create a list of attributes that can be added to chain
    # It would be cool to have some code prediction.
    self._imports = pipe(self._imports, map(module_methods), concat, filter(lambda x: hasattr(x,'__name__')),list)
    
    # Tokens record function, arguments, and keywork arguments.
    self._tokens = []
    
    # Default context to evaluate the chain.
    self._args = args
    self._kwargs = kwargs


# > Method to compose a function from the tokens that 
# have been created in the chain

# In[37]:

@new_method
def _compose(self):
    """Compose a function that can be reusable function from the tokens.
    """
    if self._tokens:
        return compose(
            *pipe(
                self._tokens,
                reversed,
                map(
                    lambda e: partial(
                        e[0], *e[1], **e[2]
                    ) if e[1] or e[2] else e[0],
                )
            )
        )
    return identity


# > `value` composes the function and then evaluate it with either 
# the default context or a new set of arguments to evaluate with the same composition.

# In[38]:

@new_method
def value(self, *args, **kwargs):
    """Compose and evaluate the function.  If no args or kwargs are provided
    then the initialized context is used.
    """
    fn = self._compose()
    if args or kwargs:
        return fn(*args, **kwargs)
    if self._kwargs: 
        return fn(*self._args, **self._kwargs)
    if self._args:
        return fn(*self._args)
    return self._tokens


# > `__call__` does not execute anything it just records args 
# and kwargs that would be passed to the function.

# In[39]:

@new_method
def __call__(self, *args, **kwargs):
    """Add args and kwargs to the tokens.
    """
    self._tokens[-1][1] = args
    self._tokens[-1][2] = kwargs
    return self


# In[40]:

@new_method
def _getter(self, attr):
    """Choose a function from the imports based on a named id.
    """
    return pipe(self._imports, filter(lambda x: x.__name__ == attr), first)


# ```python
# Chain([1,2,3,4]).reversed().str()
# ```

# In[41]:

@new_method
def __getattr__(self, attr):
    """Add a token for an attribute in _imports.
    """
    self._tokens.append([self._getter(attr), [], {}])
    return self


# > A mighty flexible way to append any function the chain.

# ```python
# Chain([1,2,3,4])[reversed][str]
# ```

# In[42]:

@new_method
def __getitem__(self, item):
    """Any function in the itme can be tokenized.
    """
    self._tokens.append([item, (), {}])
    return self


# > A `Chain` is a `Chain` until `value` or `>`.  

# > Evaluate when the repr is called.  Make sure to add a `;` to suppress output if necessary

# In[106]:

@new_method
def __repr__(self):
    return self.value().__repr__()


# ```
# XXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXChainXXXXXLinkXXXXX
# XXXXXShorthandXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXX
# ```

# In[107]:

class _X(Chain):
    """Shorthand for `Chain` where `_X.f is Chain.value`.  Typographically dense.
    """
    @property
    def f(self): return self.value


# > Copy the state of the chain and return a new one.

# In[108]:

@new_method
def copy(self):
    """Create a new instance of the current chain.  Used for 
    """
    chain = self.__class__(*self._args, **self._kwargs)
    chain._imports = self._imports[:]
    chain._tokens = self._tokens[:]
    return chain   


# ##### Some sweet ol' syntactic sugar that looks like functional programming.
# 
# > `__or__`
# 
# >   * adds a piping method to a chain.  Any functional can be included in the pipe.
# >   * is shorthand for a copy and a an append.

# In[109]:

@new_method
def __or__(self, f):
    """Extend the current chain.
    """
    chain = self.copy()
    chain._tokens.append([f, [], {}])
    return chain


# > `__gt__` is shorthand for a copy, append, and a `value` operation.

# In[110]:

@new_method
def __gt__(self, f):
    """Extend and evaluate the chain.
    """
    return self.__or__(f).value()


# In[111]:

class this(_X):
    def __getitem__(self, item):
        self._tokens.append([lambda x: x[item], [], {}])
        return self
    def __getattr__(self, item):
        self._tokens.append([lambda x: getattr(x, item), [], {}])
        return self
    def __call__(self, *args, **kwargs):
        if self._tokens:
            self._tokens[-1][0] = compose(
                lambda x: x(*args, **kwargs),
                self._tokens[-1][0],
            )
        return self


# # About the design
# 
# The goal of `Chain` is rapidly prototype code using powerful modules in the 
# Python ecosystem.  More specifically, this was designed with the intent of 
# creating data rich web applications that may work client or server side.
# 
# Applications are complex.  Fortunately, `conda` and `pip` provide lower 
# barriers to entry for building complex systems.  With this access, it is 
# possible to write functional code that spans loading through an ETL pipeline
# to an application.  This workflow was inspired greatly by `toolz` and chainable `d3`
# expressions.  Choosing these opinions greatly minimizes the need for naming.
# 
# ## Naming
# 
# Naming takes time and have the potential to confuse others.  The python ecosystem 
# provides a broad corpus to load, transform, model, and visualize data with simple
# methods to deploy them into applications or scale to other day.
# 
# I don't want to name stuff.  Also, I want to write code quicker.  Using existing namespaces
# enhances code prediction while developing in the notebook.
# 
# ## Intent
# 
# * Design a lightweight class that offers a typographically and functionally compact python syntax.
# * Maximize screen real estate for impact.  This optimizes copy and paste ability.
# * Lazy.  Most of this comes from toolz.
# * Reusability.
# * Don't create a new grammar.
# 
# ## Advantages
# 
# * Less decisions to make, better code prediction.
# * Complex operations can be isolated to a notebook cell
# * Enhanced copy and pasting abilities.
# 
# ## History
# 
# 1. Design an API that mimics [`chain` from `underscorejs`](http://underscorejs.org/#chain).  This 
# includes the `value` function that evaluates that `chain`.  `Chain` could only use `builtins` and `toolz.curried`.
# 
#     ```python
#     Chain([1,2,3]).map(lambda x: x**2).list()
#     ```
#     
#     `value` can take args and kwargs to apply a different context to the functions.
# 
#     ```python
#     c = Chain([1,2,3]).map(lambda x: x**2).list()
#     c.value([3,5,7])
#     ```
# 
# 2. Extend the API to functions in the global namespace using the `__getitem__` method.  Chaining functions
# using the attribute created a nice typographic layout.
# 
#     ```python
#     Chain([1,2,3])[
#         map(lambda x: x**2)
#     ].list()
#     ```
#     
# 3. Add syntactic sugar to extend and evaluate a chain.  
# 
#     __extend a chain__ `Chain([1,2,3]) | map(lambda x: x**2) | list`
#     
#     __evaluate a chain__ `Chain([1,2,3]) | map(lambda x: x**2) > list`

# In[112]:

# import pandas as pd
# from IPython import display
# this(pd.util.testing.makeDataFrame()).set_index('B')[['A']].to_html() > display.HTML

