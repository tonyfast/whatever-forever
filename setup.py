from os.path import join, dirname
import setuptools

def read(fname):
    with open(join(dirname(__file__), fname)) as f:
        return f.read()

setuptools.setup(
    name="whatever-forever",
    version="0.0.12",
    author="Tony Fast",
    author_email="tony.fast@gmail.com",
    description="prototype whatever in the Jupyter notebook",
    license="BSD-3-Clause",
    keywords="IPython Magic Jupyter",
    url="http://github.com/tonyfast/whatever-forever",
    packages=setuptools.find_packages(),
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