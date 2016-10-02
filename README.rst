
``whatever-forever``
====================

Create reusable, higher-order functions using declarative syntaxes in
Python.

Installation
------------

``pip install whatever-forever``

Basic Usage
-----------

Chaining in Python
~~~~~~~~~~~~~~~~~~

.. code:: python

    from whatever import *
    __my_chain = __x(5).range.map(lambda x: x+3).list
    __my_chain




.. parsed-literal::

    [3, 4, 5, 6, 7]



A random list
'''''''''''''

.. code:: python

    from random import random
    __random_list = __x(5).range.map(lambda x: random()).list.value()
    str(__random_list)




.. parsed-literal::

    '[0.10095399022711649, 0.8604968925166636, 0.008445535846122287, 0.6610363926991931, 0.6330613356373495]'



Syntactic Sugar
~~~~~~~~~~~~~~~

.. code:: python

    from random import random
    __x(__random_list.__()) * (lambda s: '%3.2f' % s) | list




.. parsed-literal::

    ['0.08', '0.06', '0.33', '0.89', '0.71']



.. code:: python

    from random import random
    ((__x(__random_list.__()) + (lambda x: x >.5) )
     * (lambda s: '%3.2f' % s) 
     | list
    )




.. parsed-literal::

    ['0.80', '0.63', '0.80', '0.64']



Development
-----------

Running the Build and Tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    pip install -r requirements-dev.txt
    python setup.py develop
    watchmedo tricks tricks.yaml

The ``watchmedo`` script will convert your notebooks to scripts and html
files. ``py.test-ipynb`` will test all notebooks matching
``test-*.ipynb``.

Running the docs
^^^^^^^^^^^^^^^^

::

    jekyll serve docs -wit

Docs are hosted at ``http://localhost:4000/whatever-forever/``.

License
-------

``whatever-forever`` is released as free software under the `BSD
3-Clause
license <https://github.com/tonyfast/whatever-forever/blob/master/LICENSE>`__.

