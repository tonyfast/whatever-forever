
# coding: utf-8

# In[ ]:

from .chain import Chain, this, _X
from .magic import magical
from . import callables

__version__ = "0.0.16"

__all__ = [
    'magical', 'this', 'callables', '_X', 'Chain',
]
