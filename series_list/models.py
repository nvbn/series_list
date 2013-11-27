import os
from .loaders.posters import IMDBPosterLoader
from .loaders.subtitles import Addic7edLoader
from . import const


class BaseModel(object):
    """Base model"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class SeriesEntry(BaseModel):
    """Series entry model"""
    cache = {}

    @classmethod
    def get_or_create(cls, **kwargs):
        if not kwargs['magnet'] in cls.cache:
            cls.cache[kwargs['magnet']] = cls(**kwargs)
        return cls.cache[kwargs['magnet']]

    def __init__(self, **kwargs):
        super(SeriesEntry, self).__init__(**kwargs)
        self.poster = IMDBPosterLoader().get_default_poster_data()
        self.subtitle = None
        self.stop_download = False

    def __repr__(self):
        return self.title

    def load_poster(self):
        """Get poster from loader"""
        self.poster = IMDBPosterLoader().get_poster_data(self.title)

    def load_subtitle(self):
        """Get subtitles from loader"""
        self.subtitle = Addic7edLoader().get_subtitle_url(self.title)

    @property
    def file_name(self):
        return u'{}.avi'.format(self.title)

    @property
    def path(self):
        return os.path.join(const.DOWNLOAD_PATH, self.file_name)

    def remove_file(self):
        """Remove downloaded file"""
        if os.path.exists(self.path):
            os.unlink(self.path)

    def update(self, other):
        """Update from other model"""
        self.poster = other.poster
        self.subtitle = other.subtitle


class Subtitle(BaseModel):
    """Subtitle model"""

    def __repr__(self):
        return self.name

    @property
    def path(self):
        return os.path.join(const.DOWNLOAD_PATH, u'{}.srt'.format(self.name))
