import abc
from ...settings import config
from ..base import BaseLoader


class SubtitlesLoader(BaseLoader):
    """Abstract subtitles loader"""

    @abc.abstractmethod
    def get_subtitle_url(self, name):
        """Get subtitle url by episode name"""

    @abc.abstractmethod
    def download(self, model):
        """Download subtitles"""

    @property
    def timeout(self):
        """Timeout for subtitles"""
        return config.subtitle_timeout
