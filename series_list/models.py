from .loaders.posters import IMDBPosterLoader
from .loaders.subtitles import Addic7edLoader


class SeriesEntry(object):
    """Series entry model"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.poster = IMDBPosterLoader().get_default_poster_data()
        self.subtitle = None

    def __repr__(self):
        return self.title

    def load_poster(self):
        """Get poster from loader"""
        self.poster = IMDBPosterLoader().get_poster_data(self.title)

    def load_subtitle(self):
        """Get subtitles from loader"""
        self.subtitle = Addic7edLoader().get_subtitle_url(self.title)


class Subtitle(object):
    """Subtitle model"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
