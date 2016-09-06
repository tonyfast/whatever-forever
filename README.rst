
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
    my_chain = Chain(5).range.map(lambda x: x+3).list
    my_chain




.. parsed-literal::

    [3, 4, 5, 6, 7]



A random list
'''''''''''''

.. code:: python

    from random import random
    random_list = _X(5).range.map(lambda x: random()).list.value()
    str(random_list)




.. parsed-literal::

    '[0.9797835854505124, 0.7465362603228028, 0.9564821512434867, 0.25918443126809687, 0.8989533853121069]'



Syntactic Sugar
~~~~~~~~~~~~~~~

.. code:: python

    from random import random
    _X(random_list) * (lambda s: '%3.2f' % s) | list




.. parsed-literal::

    ['0.98', '0.75', '0.96', '0.26', '0.90']



.. code:: python

    from random import random
    ((_X(random_list) + (lambda x: x >.5) )
     * (lambda s: '%3.2f' % s) 
     | list
    )




.. parsed-literal::

    ['0.98', '0.75', '0.96', '0.90']



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
