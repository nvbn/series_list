from decorator import decorator
from PySide.QtGui import QApplication


@decorator
def ticked(fnc, *args, **kwargs):
    """Check app tick"""
    if 'tick' in kwargs:
        tick = kwargs['tick']
    else:
        tick = args[-1]
    if tick == QApplication.instance().tick:
        return fnc(*args, **kwargs)
