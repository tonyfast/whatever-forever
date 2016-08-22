
# coding: utf-8

# In[1]:

from collections import OrderedDict
from typing import Iterable, Any

__all__ = ['Dispatch']

class Dispatch(OrderedDict):
    """An object that provides multiple dispatch when it is called.
    """
    def __call__(self, *args, **kwargs):
        for types, fn in self.items():
            if not isinstance(types, Iterable):
                types = tuple([types])
            if len(args) == len(types):
                for arg, type_ in zip(args, types):
                    if type_ != Any and not isinstance(arg, type_): break
                else:
                    return fn(*args)
        raise TypeError("Type(s) not found")

