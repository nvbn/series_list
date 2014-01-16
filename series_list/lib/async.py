from functools import partial
from decorator import decorator
from .actors import actors


@decorator
def async(fnc, *args, **kwargs):
    """Use fnc as async generator"""
    gen = fnc(*args, **kwargs)

    def perform(result):
        try:
            actor, msg, data = gen.send(result)
            actor.send(msg, perform, **data)
        except StopIteration:
            return

    perform(None)


class ActorProxy(object):
    """Actor proxy for async"""

    def __init__(self, name):
        self._actor = actors[name]

    def __getattr__(self, item):
        return partial(self._create_call, item)

    def _create_call(self, msg, **data):
        return self._actor, msg, data


class ActorsProxyManager(object):
    """Actors proxy manager"""

    def __getattr__(self, item):
        return ActorProxy(item)


proxy = ActorsProxyManager()


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
