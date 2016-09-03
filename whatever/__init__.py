
# coding: utf-8

# In[ ]:

__version_info__ = (0, 0, 15)
__version__ = '.'.join(map(str, __version_info__))

from .chain import Chain, this, _X
from .magic import magical
from . import callables

__all__ = [
    'magical', 'this', 'callables', '_X', 'Chain',
]

