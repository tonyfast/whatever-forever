
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

    from whatever4e import Forever
    from jinja2 import Template
    @Forever.cell('jinja2', lang='jinja2', display='Markdown')
    def render_jinja_with_globals(cell):
        return Template(cell).render(**globals())

License
-------

``whatever4e`` is released as free software under the [BSD 3-Clause
license]
(https://github.com/tonyfast/whatever-forever/blob/master/LICENSE).

    Add toolz.curried to global imports because I keep using it.

.. code:: python

    __version_info__ = (0, 0, 11)
    __version__ = '.'.join(map(str, __version_info__))
    
    from .chain import Chain, this, _X
    from .magic import Forever
    from class_maker import method
    from toolz.curried import *
    import toolz.curried
    
    __all__ = [
        'Forever', 'Chain', 'method', 'this', '_X', *pipe(
            toolz.curried, dir, filter(
                complement(lambda s: s.startswith('_'))
            ), list
        )
    ]
