
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

# In[6]:

from .class_maker import method
import builtins
import operator
import toolz.curried
from toolz.curried import (
    compose, filter, first, juxt, map, partial, pipe, concat, complement
)
from typing import Any, Callable, Iterable

__all__ = ['Chain', '_X', 'this',]


# In[7]:

class Chain(object): 
    _imports = [toolz.curried, operator, builtins]
    
    # compose goes here because it is in the namespace already
    @property
    def compose(self)->Callable:
        return self._composer(self._tokens)
    
new_method = method(Chain)


# ```python
# Chain([1,2]).map(lambda x: x**2).list().value()
# ```

# In[8]:

def module_methods(module)->list: 
    return pipe(module, dir, filter(
            lambda x: not x.startswith('_')
        ), map(
            partial(getattr, module)
        ), list)


# In[9]:

def composer(tokens)->Callable: 
    return compose(*pipe(tokens, reversed, filter(
            compose(bool, first,)
        ), map(
            lambda t: partial(t[0], *t[1], **t[2]) if t[1] or t[2] else t[0]
        ), list))


# In[10]:

@new_method
def __init__(
    self,
    *args, **kwargs
):  
    # An object with aliases to functions.
    self._getter = pipe(
        self._imports, reversed, map(module_methods), 
        concat, filter(lambda x: hasattr(x,'__name__')), 
        map(lambda x: (x.__name__, x)), list, dict
    ).get
    
    # Tokens record function, arguments, and keywork arguments.
    self._tokens = []
    
    # Default context to evaluate the chain.
    self._args, self._kwargs = args, kwargs
    
    # default composer
    self._composer = composer


# > `value` composes the function and then evaluate it with either 
# the default context or a new set of arguments to evaluate with the same composition.

# In[11]:

@new_method
def value(self, *args, **kwargs)->[Any, None]:
    """Compose and evaluate the function.  If no args or kwargs are provided
    then the initialized context is used.
    """
    fn = self.compose
    # If any new arguments have been supplied then use them
    if args or kwargs: return fn(*args, **kwargs)
    # If there are default kwargs
    if self._kwargs:return fn(*self._args, **self._kwargs)
    # If there is a context
    if self._args: return fn(*self._args)
    return None


# > `__call__` does not execute anything it just records args 
# and kwargs that would be passed to the function.

# In[12]:

@new_method
def __call__(self, *args, **kwargs)->Chain:
    """Add args and kwargs to the tokens.
    """
    self._tokens[-1][1:3] = args, kwargs
    return self


# ```python
# Chain([1,2,3,4]).reversed().str()
# ```

# In[13]:

@new_method
def __getattr__(self, attr)->Chain:
    """Add a token for an attribute in _imports.
    """
    self._tokens.append([self._getter(attr), [], {}])
    return self


# > A mighty flexible way to append any function the chain.

# ```python
# Chain([1,2,3,4])[reversed][str]
# ```

# In[14]:

@new_method
def __getitem__(self, item)->Chain:
    """Any function in the item can be tokenized.
    """
    if isinstance(item, Iterable): item = juxt(*item)
    self._tokens.append([item, (), {}])
    return self


# > A `Chain` is a `Chain` until `value` or `>`.  

# > Evaluate when the repr is called.  Make sure to add a `;` to suppress output if necessary

# In[15]:

@new_method
def __repr__(self)->str:
    return self.value().__repr__()


# ```
# XXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXChainXXXXXLinkXXXXX
# XXXXXShorthandXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXX
# ```

# In[16]:

class _X(Chain):
    """Shorthand for `Chain` where `_X.f is Chain.value`.  Typographically dense.
    """
    @property
    def f(self)->Any:
        return self.value


# > Copy the state of the chain and return a new one.

# In[17]:

@new_method
def copy(self, klass=None)->Chain:
    """Create a new instance of the current chain.  Used for 
    """
    chain = (klass if klass else self.__class__)(*self._args, **self._kwargs)
    chain._imports, chain._tokens = self._imports[:],  self._tokens[:]
    return chain   


# ##### Some sweet ol' syntactic sugar that looks like functional programming.
# 
# > `__or__`
# 
# >   * adds a piping method to a chain.  Any functional can be included in the pipe.
# >   * is shorthand for a copy and a an append.

# In[18]:

@new_method
def __or__(self, f)->Chain:
    """Extend the current chain.
    """
    chain = self.copy()
    chain._tokens.append([f, [], {}])
    return chain


# In[19]:

@new_method
def __mul__(self, f)->Chain:
    """Extend the current chain.
    """
    chain = self.copy()
    chain._tokens.append([map(f), [], {}])
    return chain


# In[20]:

@new_method
def __add__(self, f)->Chain:
    """Extend the current chain.
    """
    chain = self.copy()
    chain._tokens.append([filter(f), [], {}])
    return chain


# In[21]:

@new_method
def __sub__(self, f)->Chain:
    """Extend the current chain.
    """
    chain = self.copy()
    chain._tokens.append([filter(complement(f)), [], {}])
    return chain

@new_method
def __mul__(self, f)->Chain:
    """Extend the current chain.
    """
    chain = self.copy()
    chain._tokens.append([map(f), [], {}])
    return chain

@new_method
def __add__(self, f)->Chain:
    """Extend the current chain.
    """
    chain = self.copy()
    chain._tokens.append([filter(f), [], {}])
    return chain


# > `__gt__` is shorthand for a copy, append, and a `value` operation.

# In[22]:

@new_method
def __gt__(self, f)->Any:
    """Extend and evaluate the chain.
    """
    if f is compose: return self.compose
    return self.__or__(f).value()


# > `this` is a modified chain that can access items and attributes.
# 
# > Most frequently, the `f` or `value` must be called as a function closure.
# 
# ```python
# this().set_index('A').index.values.f
# this().set_index('A')[['B', 'D']].f
# ```

# In[23]:

class this(_X): pass
new_this_method = method(this)


# > Create a token to access an item.   Arbitrary functions can be applied with a `|`.

# In[24]:

@new_this_method
def __getitem__(self, item)->_X:
    self._tokens.append([lambda item, x: x[item], [item], {}])
    return self


# > Create a token to get an attribute.

# In[25]:

@new_this_method
def __getattr__(self, item)->_X:
    self._tokens.append([lambda item, x: getattr(x, item), [item], {}])
    return self


# > Create a token to call arguments and kwargs on an attribute or item.

# In[26]:

@new_this_method
def __call__(self, *args, **kwargs)->_X:
    """Add args and kwargs to the tokens.
    """
    self._tokens.append(
        [lambda args, kwargs, fn: fn(*args, **kwargs), [args, kwargs], {}]
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
