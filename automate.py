
# coding: utf-8

# ## Automation
# Nothing too fancy here.

# In[16]:

# !python setup.py register -r pypi
# !python setup.py sdist
# !python setup.py bdist_wheel
# !python setup.py sdist upload -r pypi
# !python setup.py bdist_wheel upload -r pypi


# In[14]:

# %%file setup.py
# from os.path import join, dirname
# import setuptools

# def read(fname):
#     with open(join(dirname(__file__), fname)) as f:
#         return f.read()

# setuptools.setup(
#     name="whatever-forever",
#     version="0.0.14",
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


# In[2]:

heading = """---
layout: index
---
"""


# In[10]:

import os
from glob import glob
from pyquery import PyQuery as pq
from nbconvert import export_html, export_rst
for the_script in glob('whatever/*.py'):
    with open(the_script) as f:
        src = f.read()

for the_docs in [
    *glob('whatever/*.ipynb'),
    *glob('docs/*.ipynb'), *glob('docs/**/*.ipynb')
]:
    with open(the_docs) as f:
        q = pq(export_html(the_docs)[0])
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

directory = 'docs/_layouts'
if not os.path.isdir(directory):
    makedirs(directory)

with open('docs/_layouts/index.html', 'w') as f:
    q('body').html('{{content}}', method='html')
    f.write(
        """<!doctype html><html>"""+q.html(method='html').strip()+"""</html>"""
    )
with open('README.rst', 'w') as f:
    f.write(export_rst('docs/tests/test-readme.ipynb')[0])


# ### Run tests

# In[25]:

# !flake8


# ## Test Release for PyPi
