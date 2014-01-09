from decorator import decorator


@decorator
def ticked(fnc, *args, **kwargs):
    """Check app tick"""
    from PySide.QtGui import QApplication

    if 'tick' in kwargs:
        tick = kwargs['tick']
    else:
        tick = args[-1]
    if tick == QApplication.instance().tick:
        return fnc(*args, **kwargs)


@decorator
def _lazy_for_all(fnc, self):
    """Lazy property decorator for all cls instances"""
    cls = type(self)
    attr = '_lazy_result_of_{}_for_{}'.format(fnc.__name__, cls.__name__)
    if not hasattr(cls, attr):
        setattr(cls, attr, fnc(self))
    return getattr(cls, attr)
lazy_for_all = lambda fnc: property(_lazy_for_all(fnc))


@decorator
def _lazy(fnc, self):
    """Lazy property for instance"""
    attr = '_{}'.format(fnc.__name__)
    if not hasattr(self, attr):
        setattr(self, attr, fnc(self))
    return getattr(self, attr)
lazy = lambda fnc: property(_lazy(fnc))
