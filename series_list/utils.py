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
