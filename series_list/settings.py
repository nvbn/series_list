import json
import os
from . import const


class Config(object):
    """Config object"""

    def _variable(name, default):
        @property
        def variable(self):
            return self._get_settings_dict().get(name, default)

        @variable.setter
        def variable(self, value):
            settings = self._get_settings_dict()
            settings[name] = value
            self._save_settings_dict(settings)

        return variable

    download_path = _variable('download_path', const.DOWNLOAD_PATH)

    series_timeout = _variable('series_timeout', const.SERIES_TIMEOUT)
    subtitle_timeout = _variable('subtitle_timeout', const.SUBTITLE_TIMEOUT)
    poster_timeout = _variable('poster_timeout', const.POSTER_TIMEOUT)

    posters_loader = _variable('posters_loader', const.POSTERS_LOADER)
    series_loader = _variable('series_loader', const.SERIES_LOADER)
    subtitles_loader = _variable('subtitles_loader', const.SUBTITLES_LOADER)

    preview_minimum = _variable('preview_minimum', const.PREVIEW_MINIMUM)

    def _get_settings_dict(self):
        """Get settings dict"""
        if not os.path.exists(const.SETTINGS_PATH):
            return {}
        with open(const.SETTINGS_PATH) as settings_file:
            return json.loads(settings_file.read())

    def _save_settings_dict(self, settings):
        """Save settings dict"""
        with open(const.SETTINGS_PATH, 'w') as settings_file:
            settings_file.write(json.dumps(settings))


config = Config()
