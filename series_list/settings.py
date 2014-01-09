import json
import os
from .utils import lazy
from . import const


class Var(object):
    """Descriptor for settings variable"""

    def __init__(self, default):
        self._default = default
        self._instance = None

    @lazy
    def _name(self):
        """Get name of variable"""
        for attr, value in type(self._instance).__dict__.items():
            if value == self:
                return attr

    def __get__(self, instance, owner):
        """Get settings variable"""
        self._instance = instance
        return instance.get_settings_dict().get(self._name, self._default)

    def __set__(self, instance, value):
        """Set settings variable"""
        self._instance = instance
        settings = instance.get_settings_dict()
        settings[self._name] = value
        instance.save_settings_dict(settings)


class Config(object):
    """Configuration object"""
    download_path = Var(const.DOWNLOAD_PATH)

    series_timeout = Var(const.SERIES_TIMEOUT)
    subtitle_timeout = Var(const.SUBTITLE_TIMEOUT)
    poster_timeout = Var(const.POSTER_TIMEOUT)

    posters_loader = Var(const.POSTERS_LOADER)
    series_loader = Var(const.SERIES_LOADER)
    subtitles_loader = Var(const.SUBTITLES_LOADER)

    preview_minimum = Var(const.PREVIEW_MINIMUM)

    max_retry = Var(const.MAX_RETRY)

    def get_settings_dict(self):
        """Get settings dict"""
        if not os.path.exists(const.SETTINGS_PATH):
            return {}
        with open(const.SETTINGS_PATH) as settings_file:
            return json.loads(settings_file.read())

    def save_settings_dict(self, settings):
        """Save settings dict"""
        with open(const.SETTINGS_PATH, 'w') as settings_file:
            settings_file.write(json.dumps(settings))


config = Config()
