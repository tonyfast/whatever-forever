import os
from setuptools import setup


def read(fname):
    """
    Utility function to read the README file.
    Used for the long_description.  It's nice, because now 1) we have a top
    level README file and 2) it's easier to type in the README file than to put
    a raw string in below ...
    """
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name="whatever-forever",
    version="0.0.5",
    author="Tony Fast",
    author_email="tony.fast@gmail.com",
    description="prototype whatever in the Jupyter notebook",
    license="BSD",
    keywords="IPython Magic Jupyter",
    url="http://github.com/tonyfast/whatever-forever",
    py_modules=["whatever-forever"],
    long_description=read("README.rst"),
    classifiers=[
        "Topic :: Utilities",
        "Framework :: IPython",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Testing",
    ],
    install_requires=[
        "toolz",
    ]
)