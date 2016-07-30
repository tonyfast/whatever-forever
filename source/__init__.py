
# coding: utf-8

# In[ ]:

__version_info__ = (0, 3, 0)
__version__ = '.'.join(map(str, __version_info__))

from .chain import Chain
from .magic import Whatever

__all__ = [
    'Whatever', 'Chain',
]

