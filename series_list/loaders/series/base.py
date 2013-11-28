import abc


class SeriesLoader(object):
    """Abstract series loader"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_series(self, page=0, filters=''):
        """Get series for page with filters"""
