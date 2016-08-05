
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

# In[1]:

from .class_maker import method
import builtins
import toolz.curried
from toolz.curried import *
from types import MethodType
from typing import Callable


# In[10]:

class Chain(object): 
    _imports = [toolz.curried, builtins]
    
new_method = method(Chain)


# In[17]:

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

# In[18]:

@new_method
def _compose(self):
    """From the tokens, compose a function that can be reused.
    """
    return compose(
        *pipe(
            self._tokens if self._tokens else [[identity, [], {}]],
            reversed,
            map(
                lambda e: partial(
                    e[0], *e[1], **e[2]
                ) if e[1] or e[2] else e[0],
            )
        )
    )


# > `value` composes the function and then evaluate it with either 
# the default context or a new set of arguments to evaluate with the same composition.

# In[19]:

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
    return fn(*self._args)


# > `__call__` does not execute anything it just records args 
# and kwargs that would be passed to the function.

# In[24]:

@new_method
def __call__(self, *args, **kwargs):
    self._tokens[-1][1] = args
    self._tokens[-1][2] = kwargs
    return self


# In[25]:

@new_method
def _getter(self, attr):
    """Extract a function from the imports based on a name.
    """
    return pipe(self._imports, filter(lambda x: x.__name__ == attr), first)


# ```python
# Chain([1,2,3,4]).reversed().str()
# ```

# In[30]:

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

# In[127]:

@new_method
def __getitem__(self, item):
    self._tokens.append([item, (), {}])
    return self


# > A `Chain` is a `Chain` until `value` or `|`.  

# > Evaluate when the repr is called.

# In[129]:

@new_method
def __repr__(self):
    return self.value().__str__()


# > Copy the state of the chain and return a new one.

# In[130]:

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

# In[31]:

@new_method
def __or__(self, f):
    chain = self.copy()
    chain._tokens.append([f, [], {}])
    return chain


# > `__gt__` is shorthand for a copy, append, and a `value` operation.

# In[132]:

@new_method
def __gt__(self, f):
    return self.copy()[f].value()


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

# In[ ]:



