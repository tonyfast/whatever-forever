
``whatever-forever``
====================

A generalized declarative syntax for Python objects.

Installation
------------

``pip install whatever-forever``

Basic Usage
-----------

Chain - declarative 
~~~~~~~~~~~~~~~~~~~~

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

    '[0.054198466781843035, 0.3460878567298823, 0.4675066659151689, 0.1821870800287837, 0.8590642257986899]'



.. code:: python

    from random import random
    _X(random_list) * (lambda s: '%3.2f' % s) | list




.. parsed-literal::

    ['0.99', '0.01', '0.89', '0.86', '0.30']



.. code:: python

    from random import random
    ((_X(random_list) + (lambda x: x >.5) )
     * (lambda s: '%3.2f' % s) 
     | list
    )




.. parsed-literal::

    ['0.99', '0.89', '0.86']



``magical``
-----------

Easy to construct cell magics

Cell Magics
~~~~~~~~~~~

Create a ``jinja`` to Markdown magic.

.. code:: python

    from jinja2 import Template
    @magical('jinja2', lang='jinja2', display='Markdown')
    def render_jinja_with_globals(cell):
        return Template(cell).render(**globals())

Development
-----------

Running test and the docs server.

::

    watchmedo tricks tricks.yaml
    jekyll serve docs -wit

License
-------

``whatever-forever`` is released as free software under the `BSD
3-Clause
license <https://github.com/tonyfast/whatever-forever/blob/master/LICENSE>`__.
