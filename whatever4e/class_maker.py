from toolz.curried import curry
from inspect import isclass
from types import MethodType

__all__ = [
    'add_method',
]

@curry
def method(
    class_or_instance,
    f,
    decorators = [],
):
    """Add a method to class or instance.
    """
    name, fn = f.__name__, f
    if not isclass(class_or_instance):
        fn = MethodType(fn, class_or_instance)
    for decorator in decorators:
        fn = decorator(fn)
    setattr(class_or_instance, name, fn)
    return f