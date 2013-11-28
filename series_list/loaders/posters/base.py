import abc


class PostersLoader(object):
    """Abstract posters loader"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_poster(self, name):
        """Get poster by episode name"""

    @abc.abstractmethod
    def get_poster_data(self, name):
        """Get fetched poster by name"""

    @abc.abstractmethod
    def get_default_poster_data(self):
        """Get fetched default poster"""
