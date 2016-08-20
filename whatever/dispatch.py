
# coding: utf-8

# In[76]:

from itertools import zip_longest
from toolz.curried import (
    compose, filter, first, identity, juxt, last,
    map, partial, pipe, second, valmap
)
from collections import OrderedDict
from typing import Iterable

__all__ = ['Dispatch']

class Dispatch(OrderedDict):
    """An object that provides multiple dispatch when it is called.
    """
    def __getattr__(self, attr):
        print(attr)
        return super().__getattr__(attr)

    def __call__(self, *args, **kwargs):
        fns = pipe(
                self, map(
                    juxt(lambda x: x if isinstance(x, Iterable) else tuple([x]),
                        self.get, identity,)),
                map(
                    lambda x: [pipe(x[0], partial(zip_longest, args), list), *x[1:]]
                ),
                filter(compose(lambda x: len(x) == len(args), first)), 
                list,
            )        
        if fns:
            return pipe(fns, first, second)(*args)

        raise TypeError("Type not found")

