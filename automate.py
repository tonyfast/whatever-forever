
# coding: utf-8

# ## Automation
# Nothing too fancy here.

# In[58]:

# %%file setup.py
# from os.path import join, dirname
# import setuptools

# def read(fname):
#     with open(join(dirname(__file__), fname)) as f:
#         return f.read()

# setuptools.setup(
#     name="whatever-forever",
#     version="0.0.12",
#     author="Tony Fast",
#     author_email="tony.fast@gmail.com",
#     description="prototype whatever in the Jupyter notebook",
#     license="BSD-3-Clause",
#     keywords="IPython Magic Jupyter",
#     url="http://github.com/tonyfast/whatever-forever",
#     packages=setuptools.find_packages(),
#     long_description=read("README.rst"),
#     classifiers=[
#         "Topic :: Utilities",
#         "Framework :: IPython",
#         "Natural Language :: English",
#         "Programming Language :: Python",
#         "Intended Audience :: Developers",
#         "Development Status :: 3 - Alpha",
#         "Operating System :: OS Independent",
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: BSD License",
#         "Topic :: Software Development :: Testing",
#     ],
#     install_requires=[
#         "toolz",
#     ]
# )


# In[22]:

heading = """---
layout: index
---
"""


# In[48]:

from lxml.html import HTMLParser, fromstring
UTF8_PARSER = HTMLParser(encoding='utf-8')


# In[ ]:




# In[56]:

import os
from glob import glob
from pyquery import PyQuery as pq
from nbconvert import export_html
for the_script in glob('whatever/*.py'):
    with open(the_script) as f:
        src = f.read()

for the_docs in [
    *glob('whatever/*.ipynb'),
    *glob('docs/*.ipynb'), *glob('docs/**/*.ipynb')
]:
    with open(the_docs) as f:
        q = pq(fromstring(export_html(the_docs)[0], parser=UTF8_PARSER))
    path = the_docs.split('/')
    fn = path[-1]
    if path[0] == 'whatever':
        path[0] = 'docs/source'
    directory = '/'.join(path[:-1])
    if not os.path.isdir(directory):
        makedirs(directory)
    with open(directory+'/'+fn.replace('.ipynb','.html'), 'w') as f:
        f.write(
            heading
            + ("{}" if 'index.ipynb' == fn else """{{% raw %}}{}{{% endraw %}}""").format(
                    q('body').html())
            )
        if fn == 'index.ipynb':
            break
        


# In[57]:

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
