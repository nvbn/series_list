from .loaders.posters import IMDBPosterLoader
from .loaders.subtitles import Addic7edLoader


class BaseModel(object):
    """Base model"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class SeriesEntry(BaseModel):
    """Series entry model"""

    def __init__(self, **kwargs):
        super(SeriesEntry, self).__init__(**kwargs)
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


class Subtitle(BaseModel):
    """Subtitle model"""
