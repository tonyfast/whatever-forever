
# coding: utf-8

# In[1]:

from collections import OrderedDict
from toolz.curried import flip, identity, juxt, map, partial, pipe, valmap
from types import LambdaType
from typing import Iterable, Any

__all__ = ['Dispatch', 'DictCallable', 'TupleCallable', 'ListCallable', 'SetCallable']


# In[2]:

class Dispatch(OrderedDict):
    """An object that provides multiple dispatch when it is called.
    """
    def __init__(self, args=[], catch=None):
        super().__init__(args)
        if catch:
            self[Any] = catch
    def __call__(self, *args, **kwargs):
        for types, fn in self.items():
            if not isinstance(types, Iterable):
                types = tuple([types])
            if len(args) == len(types):
                for arg, type_ in zip(args, types):
                    if type_ != Any and not isinstance(arg, type_): break
                else:
                    return fn(*args, **kwargs)
        raise TypeError("Type(s) not found")


# In[3]:

class Condictional(OrderedDict):
    """An object that provides multiple dispatch when it is called.
    """
    def __init__(self, args=[], catch=identity):
        super().__init__(args)
        self[lambda *args, **kwargs: True] = catch
        
    def __call__(self, *args, **kwargs):
        for condition, fn in self.items():
            if condition(*args, **kwargs):
                return fn(*args, **kwargs)


# In[4]:

class DictCallable(dict):
    def __call__(self, *args, **kwargs):
        return valmap(
            lambda x: x(*args, **kwargs), self
        )


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

