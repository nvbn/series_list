import abc


class SubtitlesLoader(object):
    """Abstract subtitles loader"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_subtitle_url(self, name):
        """Get subtitle url by episode name"""
