import abc
from ...settings import config
from ..base import BaseLoader


class PostersLoader(BaseLoader):
    """Abstract posters loader"""

    @abc.abstractmethod
    def get_poster(self, name):
        """Get poster by episode name"""

    @abc.abstractmethod
    def get_poster_data(self, name):
        """Get fetched poster by name"""

    @abc.abstractmethod
    def get_default_poster_data(self):
        """Get fetched default poster"""

    @property
    def timeout(self):
        """Timeout for downloading posters"""
        return config.poster_timeout
