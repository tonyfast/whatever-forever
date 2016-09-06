# coding: utf-8

# In[212]:

from whatever.callables import (
    SetCallable, TupleCallable, ListCallable, DictCallable, Dispatch
)
import builtins
from joblib import Parallel, delayed
import operator
import toolz.curried
from toolz.curried import (
    complement, compose, filter,
    first, identity, juxt, map, partial,
    peek, pipe, merge, last, second,
)
from typing import Any, Callable, Iterable

__all__ = ['Chain', '_X', '_P', 'this', ]


# In[83]:

def evaluate(args, kwargs, fn):
    return fn(*args, **kwargs)


class DefaultComposer(object):
    attrs = pipe(
        [toolz.curried, builtins, operator], reversed,
        map(vars), merge,
    )

    def item(self, item):
        return item

    def attr(self, item):
        return self.attrs.get(item)

    def call(self, tokens, *args, **kwargs):
        tokens[-1][1:] = args, kwargs
        return tokens

    def composer(self, tokens):
        return compose(*pipe(
            tokens, reversed, filter(first), map(
                lambda arg: partial(arg[0], *arg[1], **
                                    arg[2]) if any(arg[1:]) else arg[0]
            ), list
        ))


# In[175]:

class Chain(object):
    _composer = DefaultComposer()

    def __init__(self, *args, **kwargs):
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
        if (
            not isinstance(attr, Callable) and
            isinstance(attr, Iterable) and
            isinstance(peek(attr), Iterable)
        ):
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
        """Create a new instance of the current chain.
        """
        chain = (klass if klass else self.__class__)(
            *self._args, **self._kwargs)
        chain._tokens = self._tokens.copy()
        return chain

    @property
    def compose(self):
        return self._composer.composer(self._tokens)

    def __dir__(self):
        return self._composer.attrs.keys()

    def __repr__(self):
        return self.value().__repr__()


# In[85]:

class SugarComposer(DefaultComposer):
    multiple_dispatch = Dispatch([
        [Callable, identity],
        [set, SetCallable],
        [list, ListCallable],
        [tuple, TupleCallable],
        [dict, DictCallable],
        [Any, identity], ])

    def item(self, item):
        return self.multiple_dispatch(item)

    def call(self, tokens, *args, **kwargs):
        if pipe(tokens, last, first) is map:
            if kwargs and not args:
                args = [kwargs]
            return super().call(
                tokens, pipe(
                    args, first, self.item,
                ),
            )
        return super().call(tokens, *args, **kwargs)


# In[86]:

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
        return self.copy().map(
            self._composer.item(f)
        )

    def __add__(self, f):
        """Filter values that are true.
        """
        return self.copy().filter(
            self._composer.item(f)
        )


# In[154]:

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


# In[201]:

class this(_X):
    """Access attributes and items of an object.
    """
    _composer = ThisComposer()

    def __init__(self, arg=None,):
        """Accepts one input argument.
        """
        super().__init__(arg)

    @property
    def f(self):
        return self.value

    @property
    def __dir__(self):
        return pipe(self._args, first).__dir__

    def copy(self, klass=_X):
        """A new chain beginning with the current chain tokens and argument.
        """
        chain = super().copy()
        new_chain = klass(chain._args[0])
        new_chain._tokens = [[
            chain.compose, [], {},
        ]]
        return new_chain

    def __repr__(self):
        self._tokens = pipe(
            self._tokens, filter(
                compose(complement(
                    lambda s: s.startswith('_ipython') or
                        s.startswith('_repr') if isinstance(s, str) else s,
                        ), first, second,)
            ), list
        )
        return self.value().__repr__()


# In[ ]:

class ParallelComposer(SugarComposer):

    def __init__(self, n_jobs=4):
        self.n_jobs = n_jobs

    def composer(self, tokens, **kwargs):
        rekey = []
        for i, token in enumerate(tokens):
            token = [token]
            if first(token[0]) is map:
                token[0][1] = [
                    delayed(token[0][1][0])
                ]
                token.append([
                    Parallel(n_jobs=self.n_jobs), [], {}
                ])
            rekey.extend(token)
        return super().composer(rekey)


# In[ ]:

class _P(_X):

    def __init__(self, *args, n_jobs=4, **kwargs):
        self._composer = ParallelComposer(n_jobs=n_jobs)
        super().__init__(*args, **kwargs)
