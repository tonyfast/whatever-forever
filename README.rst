
.. code:: python

    from whatever import *

``whatever-forever``
====================

-  Syntactic sugar to build complex functions in Python; it's just a
   class.
-  Multiple dispatching ``dict``\ s.
-  Stupid easy cell magics.

Chaining
========

``Chain`` and ``_X``

.. code:: python

    Chain(5).range.list




.. parsed-literal::

    [0, 1, 2, 3, 4]



.. code:: python

    _X(5) | range | list




.. parsed-literal::

    [0, 1, 2, 3, 4]



A random list
'''''''''''''

.. code:: python

    from random import random
    random_list = _X(5).range | map(lambda x: random()) > list
    str(random_list)




.. parsed-literal::

    '[0.9935285316596995, 0.014724817177512728, 0.8948846635050951, 0.8599661767263426, 0.2981499631390274]'



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


