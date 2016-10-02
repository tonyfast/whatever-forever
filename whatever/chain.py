# coding: utf-8

# In[1]:

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
    peek, pipe, merge, last, second, valfilter, keyfilter
)
from typing import Any, Callable, Iterable

__all__ = ['chain', 'Chain', '_x', '__x', '__p', '_this', 'compose']


# In[2]:

def evaluate(args, kwargs, fn):
    """Evaluates `fn` with the `args` and `kwargs` as unique arguments.
    """
    return fn(*args, **kwargs)


class ComposerBase(object):

    def __init__(
        self, **kwargs
    ):
        self.attrs = pipe(
            self.imports, reversed,
            map(vars), merge, keyfilter(
                compose(str.islower, first),
            ), valfilter(callable),
        )
        self.attrs.update(

        )


class DefaultComposer(ComposerBase):
    imports = [
        toolz.curried, builtins, operator
    ]

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
                lambda arg: partial(arg[0], *arg[1], **arg[2])
                if any(arg[1:]) else arg[0]
            ), list
        ))


# In[3]:

class ChainBase(object):

    def compute(self, fn, *args, **kwargs):
        # If any new arguments have been supplied then use them
        return fn(*args, **kwargs)

    def __dir__(self):
        return super().__dir__() + self._dir

    def _tokenize(self, composer, attr):
        attr = composer(attr)
        if (
            not isinstance(attr, Callable) and
            isinstance(attr, Iterable) and
            isinstance(peek(attr), Iterable)
        ):
            return attr
        return [[attr, [], ()]]


# In[4]:

class Chain(ChainBase):
    _composer = DefaultComposer()
    _dir = []

    def __init__(self, *args, **kwargs):
        # Tokens record function, arguments, and keywork arguments.
        self._tokens = []

        # Default context to evaluate the chain.
        self._args, self._kwargs = args, kwargs

    def compute(self, *args, **kwargs)->[Any, None]:
        """Compose and evaluate the function.
        """
        return super().compute(
            self.compose, *args, **kwargs
        )

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
        chain = (
            klass if klass else self.__class__
        )(*self._args, **self._kwargs)
        chain._tokens = self._tokens.copy()
        return chain

    @property
    def compose(self):
        return self._composer.composer(self._tokens)

    def __dir__(self):
        return super().__dir__() + list(self._composer.attrs.keys())


# In[5]:

class chain(Chain):

    def __repr__(self):
        if self._args or self._kwargs:
            return self.compute(
                *self._args, **self._kwargs,
            ).__repr__()
        func = self.compose
        return '\n'.join([
            str(func.first),
            func.funcs.__repr__(),
        ])


# In[6]:

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


# In[7]:

class LiterateAPI(chain):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _len = pipe(
            self.__class__.__name__,
            map(str.isalnum),
            list,
            lambda x: x.index(True),
        )
        setattr(self, '_' * _len, self.compute)


# In[8]:

def juxtapose(func, x):
    return juxt(*func)(x)


class _x(LiterateAPI):
    """Initialize a chain delimited with single underscores.
    """
    _composer = SugarComposer()

    def __or__(self, f):
        """Extend the current chain.
        """
        return self.copy()[f]

    def __gt__(self, f)->[compose, Any]:
        """Extend and evaluate the chain.
        """
        if f is compose:
            # return toolz.compose
            return self.compose

        return self.copy()[f].compute()

    def compute(self, *args, **kwargs):
        if not(args or kwargs):
            args, kwargs = self._args, self._kwargs
        return super().compute(*args, **kwargs)

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


# In[9]:

class __x(_x):

    def _(self, *args, **kwargs):
        raise AttributeError(
            "Compose this function using a dunder - __"
        )


# In[10]:

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


# In[11]:

class _this(_x):
    """A chain object to access attributes and items.   Converts to 
    a chain when copied
    """
    _composer = ThisComposer()

    def __init__(self, arg=None,):
        """Accepts one input argument.
        """
        super().__init__(arg)

    @property
    def __dir__(self):
        return super().__dir__() + pipe(self._args, first).__dir__

    def copy(self, klass=_x):
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
        return super().__repr__()


# In[12]:

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


# In[13]:

class __p(__x):

    def __init__(self, *args, n_jobs=1, **kwargs):
        self._composer = ParallelComposer(
            n_jobs=n_jobs
        )
        super().__init__(*args, **kwargs)
