import abc


class SeriesLoader(object):
    """Abstract series loader"""
    __metaclass__ = abc.ABCMeta
    can_change_page_with_filter = True

    @abc.abstractmethod
    def get_series(self, page=0, filters=''):
        """Get series for page with filters"""

    @property
    def error_message(self):
        """Error message if loader fails"""
        return u'Something wrong with {}, ' \
               u'try switch to another series provider'\
            .format(type(self).__name__)
