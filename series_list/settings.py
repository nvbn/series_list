from PySide.QtGui import QApplication
from . import const


class Config(object):
    """Config object"""

    def _variable(name, default):
        @property
        def variable(self):
            return QApplication.instance().settings.value(name, default)

        @variable.setter
        def variable(self, value):
            return QApplication.instance().settings.setValue(name, value)

        return variable

    download_path = _variable('download_path', const.DOWNLOAD_PATH)
    series_timeout = _variable('series_timeout', const.SERIES_TIMEOUT)
    subtitle_timeout = _variable('subtitle_timeout', const.SUBTITLE_TIMEOUT)
    poster_timeout = _variable('poster_timeout', const.POSTER_TIMEOUT)


config = Config()
