
# coding: utf-8

# ## Automation
# Nothing too fancy here.

# In[16]:

# !python setup.py register -r pypi
# !python setup.py sdist
# !python setup.py bdist_wheel
# !python setup.py sdist upload -r pypi
# !python setup.py bdist_wheel upload -r pypi


# In[ ]:

import os
from glob import glob
from pyquery import PyQuery as pq
from nbconvert import export_html, export_rst


# In[ ]:

for the_docs in [
    *glob('whatever/*.ipynb'),
    *glob('docs/*.ipynb'), *glob('docs/**/*.ipynb')
]:
    with open(the_docs) as f:
        q = pq(export_html(the_docs)[0])
    path = the_docs.split('/')
    fn = path[-1]
    if path[0] == 'readme.ipynb':
        path[0] = 'docs'
    if path[0] == 'whatever':
        path[0] = 'docs/source'
    directory = '/'.join(path[:-1])
    if not os.path.isdir(directory):
        makedirs(directory)
    with open(directory+'/'+fn.replace('.ipynb','.html'), 'w') as f:
        f.write(
            """---
layout: index
---
""" + ("{}" if 'index.ipynb' == fn else """{{% raw %}}{}{{% endraw %}}""").format(
                    q('body').html(method='html'))
            )


# In[10]:

directory = 'docs/_layouts'
if not os.path.isdir(directory):
    makedirs(directory)

with open('docs/_layouts/index.html', 'w') as f:
    q('body').html('{{content}}', method='html')
    f.write(
        """<!doctype html><html>"""+q.html(method='html').strip()+"""</html>"""
    )


# ### Run tests

# In[25]:

# !flake8


# ## Test Release for PyPi
