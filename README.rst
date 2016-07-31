
Whatever Forever
================

Pythonic syntaxes that save pixels when developing in the notebook.

``Chain``
---------

A chain is a typographically compact manner of creating complicated
expressions in Pythonic syntax.

Chainable Values
~~~~~~~~~~~~~~~~

.. code:: python

    some_expr = Chain([1,2,3]).reversed().map(lambda x: x**2).list()
    some_expr.value()
    some_expr.value([3,5,8])

Syntactic Sugar
~~~~~~~~~~~~~~~

``\`` & ``>`` offer chain new functions and evaluate them respectively.

.. code:: python

    from toolz.curried import *
    some_expr = Chain([1,2,3]) | reversed | map(lambda x: x**2) | list
    some_value = Chain([1,2,3]) | reversed | map(lambda x: x**2) > list

``Whatever``
------------

Easy to construct cell magics

Cell Magics
~~~~~~~~~~~

Create a ``jinja`` to Markdown magic.

.. code:: python

    from jinja2 import Template
    @Whatever.cell('jinja2', lang='jinja2', display='Markdown')
    def render_jinja_with_globals(cell):
        return Template(cell).render(**globals())

``method``
----------

A decorator for modifying classes and instances.

.. code:: python

    class Foo:
        pass

    @method(Foo)
    def Bar(self, i=1):
        return i*2

    f = Foo()

    @method(f)
    def Bar(self, i=1):
        return i*3

License
-------

``whatever4e`` is released as free software under the [BSD 3-Clause
license]
(https://github.com/tonyfast/whatever-forever/blob/master/LICENSE).

.. code:: python

    __version_info__ = (0, 3, 0)
    __version__ = '.'.join(map(str, __version_info__))
    
    from .chain import Chain
    from .magic import Whatever
    from class_maker import method
    
    __all__ = [
        'Whatever', 'Chain', 'method',
    ]
