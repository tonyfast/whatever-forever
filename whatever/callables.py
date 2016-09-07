# coding: utf-8

# In[6]:

from collections import OrderedDict
from toolz.curried import flip, juxt, map, partial, pipe, valmap
from types import LambdaType
from typing import Iterable, Any

__all__ = [
    'Dispatch', 'DictCallable', 'TupleCallable', 'ListCallable', 'SetCallable'
]


# In[4]:

class DictCallable(dict):

    def __call__(self, *args, **kwargs):
        return valmap(
            lambda x: x(*args, **kwargs), self
        )


# In[44]:

class Condictional(OrderedDict):
    """First key to satisfy the key condition executes.
    """

    def key(self, x, *args, **kwargs)->bool:
        return x(*args, **kwargs)

    def __init__(self, args=[], default=None, key=None):
        super().__init__(args)
        self.default = default
        if key:
            self.key = key

    def __call__(self, *args, **kwargs):
        for key, value in self.items():
            if self.key(key, *args, **kwargs):
                return value(*args, **kwargs)
        if self.default:
            return self.default(*args, **kwargs)
        raise KeyError("No conditions satisfied")


# In[27]:

class Dispatch(Condictional):
    """An object that provides multiple dispatch when it is called.
    """

    def key(self, key, *args, **kwargs):
        if not isinstance(key, Iterable):
            key = tuple([key])
        if len(args) == len(key):
            return all(
                isinstance(arg, types) for arg, types in zip(args, key)
                if isinstance(types, Iterable) or types != Any
            )
        return False

    def __init__(self, args=[], default=None):
        super().__init__(args)
        self.default = default


# In[5]:

class ListCallable(list):

    def __call__(self, *args, **kwargs):
        return list(juxt(*self)(
            *args, **kwargs
        ))


# In[6]:

class SetCallable(set):

    def __call__(self, *args, **kwargs):
        if pipe(self, map(
                partial(flip(isinstance), LambdaType)
        ), any):
            raise TypeError("Cannot interpolate a LambdaType.")

        return pipe(
            zip(
                self, list(map(lambda x: x(*args, **kwargs), self))
            ), list, dict
        )


# In[7]:

class TupleCallable(tuple):

    def __call__(self, *args, **kwargs):
        return juxt(*self)(
            *args, **kwargs
        )
