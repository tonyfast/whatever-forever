
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

# In[26]:

from .callables import SetCallable, TupleCallable, ListCallable, DictCallable, Dispatch
import builtins
import operator
import toolz.curried
from toolz.curried import (
    complement, compose, concat, do, filter, 
    first, flip, identity, juxt, last, map, merge, partial, 
    peek, pipe, second, valfilter, valmap, keyfilter,
)
from typing import Any, Callable, Iterable
from collections import OrderedDict
from types import LambdaType, MethodType

__all__ = ['Chain', '_X', 'this',]


# ```python
# Chain([1,2]).map(lambda x: x**2).list().value()
# ```

# In[27]:

def import_functions(module): 
    return pipe(
        module, dir, map(partial(getattr, module)),
        filter(partial(flip(hasattr), '__name__')),
    )


# In[28]:

def evaluate(args, kwargs, fn):
    return fn(*args, **kwargs)

class DefaultComposer(object):
    keyed_methods = pipe([
            toolz.curried, builtins, operator
        ], map(import_functions), concat, map(juxt(
            partial(flip(getattr), '__name__'), identity
        )), list,  reversed, dict, keyfilter(compose(str.islower, first)), valfilter(callable))
    
    def item(self, item):
        return item
    
    def attr(self, item):
        return self.keyed_methods.get(item)
    
    def call(self, tokens, *args, **kwargs):
        tokens[-1][1:] = args, kwargs
        return tokens
    
    def composer(self, tokens):
        return compose(*pipe(
            tokens, reversed, filter(first), map(
                lambda arg: partial(arg[0], *arg[1], **arg[2]) if any(arg[1:]) else arg[0]
            ), list
        ))


# In[29]:

class Repr(object):
    def __repr__(self):
        return self.value().__repr__()


# In[30]:

class Chain(Repr): 
    _composer = DefaultComposer()
    
    def __init__(
        self,
        *args, 
        **kwargs
    ):  
        # Tokens record function, arguments, and keywork arguments.
        self._tokens = []
        
        # Default context to evaluate the chain.
        self._args, self._kwargs = args, kwargs

    def value(self, *args, **kwargs)->[Any, None]:
        """Compose and evaluate the function.  If no args or kwargs are provided
        then the initialized context is used.
        """
        fn = self._composer.composer(self._tokens)
        
        # If any new arguments have been supplied then use them
        if args or kwargs: 
            return fn(*args, **kwargs)
        
        # If there are default kwargs
        if self._kwargs:
            return fn(*self._args, **self._kwargs)
        
        # If there is a context
        if self._args: 
            return fn(*self._args)

        return None
    
    def _tokenize(self, composer, attr):
        attr = composer(attr)
        if not isinstance(attr, Callable) and isinstance(attr, Iterable) and isinstance(peek(attr), Iterable):
            return attr
        return [[attr, [], ()]]

    def __getattr__(self, attr):
        """Apply the attribute getter
        """
        self._tokens.extend(
            self._tokenize(self._composer.attr, attr)
        )
        return self
    
    def __getitem__(self, item):
        """Any function in the item can be tokenized.
        """
        self._tokens.extend(
            self._tokenize(self._composer.item, item)
        )

        return self
    
    def __call__(self, *args, **kwargs):
        self._tokens = self._composer.call(
            self._tokens, *args, **kwargs
        )
        return self
    
    def copy(self, klass=None):
        """Create a new instance of the current chain.  Used for 
        """
        chain = (klass if klass else self.__class__)(*self._args, **self._kwargs)
        chain._tokens = self._tokens.copy()
        return chain
    
    @property
    def compose(self):
        return self._composer.composer(self._tokens)
    
    def __dir__(self):
        return self._composer.keyed_methods.keys()


# ```
# XXXXXXXXXXXXXXXXXXXXXXXXXX
# XXXXXXXChainXXXXXLinkXXXXX
# XXXXXShorthandXXXXXXXXXXXX
# XXXXXXXXXXXXXXXXXXXXXXXXXX
# ```

# > Copy the state of the chain and return a new one.

# ##### Some sweet ol' syntactic sugar that looks like functional programming.
# 
# > `__or__`
# 
# >   * adds a piping method to a chain.  Any functional can be included in the pipe.
# >   * is shorthand for a copy and a an append.

# > `this` is a modified chain that can access items and attributes.
# 
# > Most frequently, the `f` or `value` must be called as a function closure.
# 
# ```python
# this().set_index('A').index.values.f
# this().set_index('A')[['B', 'D']].f
# ```

# In[31]:

class SugarComposer(DefaultComposer):    
    multiple_dispatch = Dispatch([
        [Callable, identity],
        [set, SetCallable],
        [list, ListCallable],                
        [tuple, TupleCallable],                                
        [dict, DictCallable],
        [Any, identity],])
    
    def item(self, item):
        return self.multiple_dispatch(item)    
    
    def call(self, tokens, *args, **kwargs):
        if tokens[-1][0] in [map]:
            if kwargs and not args: args = [kwargs]
            return super().call(tokens, self.item(args[0]))
        return super().call(tokens, *args, **kwargs)


# In[32]:

def juxtapose(func, x): 
    return juxt(*func)(x)

class _X(Chain):
    """Shorthand for `Chain` where `_X.f is Chain.value`.  Typographically dense.
    """
    _composer = SugarComposer()
    
    @property
    def f(self)->Callable:
        return self.value
    
    def __or__(self, f):
        """Extend the current chain.
        """
        return self.copy()[f]

    def __gt__(self, f)->Any:
        """Extend and evaluate the chain.
        """
        if f is compose: 
            return self.compose
        return self.copy()[f].value()
    
    def __mul__(self, f):
        """Apply a map function.
        """
        return self.copy().map(f)
        
    def __add__(self, f):
        """Filter values that are true.
        """
        return self.copy().filter(self._composer.item(f))


# In[33]:

def getitem(item, obj): 
    return obj[item]

def getattr_(item, obj):
    return getattr(obj, item)

class ThisComposer(DefaultComposer): 
    def item(self, item):
        return [[getitem, [item], {}]]
    
    def attr(self, item):
        return [[getattr_, [item], {}]]
    
    def call(self, tokens, *args, **kwargs):
        """Add args and kwargs to the tokens.
        """
        tokens.append([evaluate, [args, kwargs], {}])
        return tokens


# In[63]:

class this(Chain): 
    _composer = ThisComposer()
    
    @property
    def chain(self, chain_type=_X): return chain_type(self.value())
    
    @property
    def f(self): return self.value
    
    def __dir__(self): return []


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
