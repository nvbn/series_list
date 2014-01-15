from collections import defaultdict


class Observable(object):
    """Add ability to observer changes"""

    def __init__(self):
        self._observers = defaultdict(lambda: [])

    def __setattr__(self, key, value):
        super(Observable, self).__setattr__(key, value)
        if not key.startswith('_'):
            for observer in self._observers[key]:
                observer(value)

    def subscribe(self, key, callback):
        self._observers[key].append(callback)
        callback(getattr(self, key, None))
