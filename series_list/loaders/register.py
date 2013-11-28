from ..settings import config


class TypedRegister(object):
    """Typed loaders register"""

    def __init__(self, settings_name):
        self._settings_name = settings_name
        self._items = {}
        self._instances = {}

    def __call__(self, cls):
        """Register loader"""
        self._items[cls.__name__] = cls
        return cls

    def _get_instance(self, cls):
        """Get instance of loader"""
        if not cls in self._instances:
            self._instances[cls] = cls()
        return self._instances[cls]

    @property
    def _active(self):
        """Get active loader"""
        return self._get_instance(
            self._items[getattr(config, self._settings_name)],
        )

    def __getattr__(self, item):
        """Proxy to active loader"""
        return getattr(self._active, item)

    @property
    def names(self):
        """Get names of registered loaders"""
        return self._items.keys()


class Register(object):
    """Loaders register"""
    posters = TypedRegister('posters_loader')
    series = TypedRegister('series_loader')
    subtitles = TypedRegister('subtitles_loader')

    def import_all(self):
        """Import all loaders"""
        from . import posters, series, subtitles


library = Register()
