
# coding: utf-8

# # Polymorphisms

# In[34]:

from whatever import * # == from toolz.curried import *; from whatever import _X, Chain, Forever


# ## Chain
# 
# The base class to compose fucntions.

# In[2]:

from toolz.curried import *


# In[3]:

@curry
def compare(composed, composition, value):
    assert composed.value(value) == composition(value)


# In[4]:

f = Chain(10).range.list
compare(f, compose(list, range), 20)
f


# In[5]:

f = Chain(10).range(5).list
compare(f, compose(list, partial(range, 5)), 20)
f


# In[6]:

f = Chain(10)[range](5)[list]
compare(f, compose(list, partial(range, 5)))
f


# ## Shorthand

# In[7]:

g = lambda x: x**2
f = _X(10).range.map(g).list
compare(f, compose(list, map(g), range))(20)
f


# In[8]:

g = lambda x: x**2
f = _X(10).range(4).map(g).list
compare(f, compose(list, map(g), partial(range, 4)))(20)
f


# In[9]:

g = lambda x: x**2
f = _X(10).range(4) * g | list
compare(f, compose(list, map(g), partial(range, 4)))(20)
f


# In[12]:

g = lambda x: x**2
f = _X(10).range(4) * g - (lambda x: x< 20) | list
compare(f, compose(list, filter(complement(lambda x: x< 20)), map(g), partial(range, 4)))(20)
f


# In[13]:

g = lambda x: x**2
f = _X(10).range(3) * g + (lambda x: x< 20) | list
compare(f, compose(list, filter(lambda x: x< 20), map(g), partial(range, 3)))(20)
f


# ## Complex Arguments

# # Lists

# In[14]:

_X(10).range | [sum, list, len]


# In[15]:

f = _X(10).range[[sum, list, len]]
compare(f, compose(juxt(sum, list, len), range))(20)
f


# In[16]:

f = _X(10).range | [sum, list, len]
compare(f, compose(juxt(sum, list, len), range))(20)
f


# In[17]:

_X(10).range[[sum, list, len]] * type * do(print) | list


# # Dict

# In[18]:

_X(10).range[{'a': sum, 'b': list, 'c': len}]


# In[19]:

_X(10).range | {'a': sum, 'b': list, 'c': len}


# # sets

# In[20]:

_X(10).range[{sum, list, len}]


# In[21]:

d = _X(10).range | {sum, list, len}
d


# In[22]:

d | this().keys().f | list


# ## Values

# In[23]:

Chain(10).range.list.value()


# In[24]:

_X(10).range.list.f()


# In[25]:

_X(10).range.list.value()


# In[26]:

_X(10).range.list > identity


# In[27]:

_X(10) | range | list > identity


# ## Composition

# In[28]:

f = Chain(10).range.list.value
f(4)


# In[29]:

f = _X(10).range.list.f
f(4)


# In[30]:

f = _X(10).range.list.value
f(4)


# In[31]:

f = _X(10).range.list > compose
f(4)


# In[32]:

f = _X(10) | range | list > compose
f(4)


# In[ ]:



