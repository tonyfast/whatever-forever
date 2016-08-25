
# coding: utf-8

# In[ ]:

__version_info__ = (0, 0, 14)
__version__ = '.'.join(map(str, __version_info__))

from .chain import Chain, this, _X
from .magic import magical
from .callables import Dispatch
from toolz.curried import *
import toolz.curried

__all__ = [
    'magical', 'Chain', 'this', 'Dispatch', '_X', *pipe(
        toolz.curried, dir, filter(
            complement(lambda s: s.startswith('_'))
        ), list
    )
]

