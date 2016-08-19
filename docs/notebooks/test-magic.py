
# coding: utf-8

# In[ ]:

from whatever import *


# In[33]:

magical('markdown', identity)


# In[34]:

get_ipython().run_cell_magic('markdown', '', '\n# This is markdown')


# In[5]:

from yaml import safe_load
magical('yaml', safe_load, display=print)


# In[7]:

get_ipython().run_cell_magic('yaml', 'a', 'foo: \n    - bar\n    - baz')


# In[10]:

assert a == {'foo': ['bar', 'baz']}


# In[14]:

get_ipython().run_cell_magic('yaml', 'data', 'foo: bar\nbaz: yee-haw')


# In[29]:

from mistune import markdown
from jinja2 import Template
from IPython import display
magical('mistune', Template, display=lambda x:pipe(
        x.render(**globals()), display.Markdown, display.display 
    ))


# ## `jinja` magic

# In[30]:

get_ipython().run_cell_magic('mistune', '', '# This is markdown\n\nIt is rendered into HTML by python.\n\nIt can access global variables.  \n\n{% for key, value in data.items() %}* __{{key}}__ - {{value}}\n{% endfor %}')


# ## `jinja` alternate jinja magic

# In[31]:

from jinja2 import Template
magical('jinja', Template, display=lambda x: pipe(
        x.render(**globals()), display.Markdown, display.display
    ))


# In[32]:

get_ipython().run_cell_magic('jinja', '', '# This markdown is rendered by the notebook in the browser\n\nIt can __ALSO__ access global variables.  \n\n{% for key, value in data.items() %}* __{{key}}__ - {{value}}\n{% endfor %}')

