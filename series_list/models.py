import os
from glob import glob
from .lib.async import async, proxy
from .loaders import library
from .settings import config
from .lib.reactive import Observable
from .lib.models import BaseModel
from . import const


class SeriesEntry(Observable, BaseModel):
    """Series entry model"""
    cache = {}

    @classmethod
    def get_or_create(cls, **kwargs):
        if not kwargs['magnet'] in cls.cache:
            cls.cache[kwargs['magnet']] = cls(**kwargs)
        return cls.cache[kwargs['magnet']]

    def __init__(self, **kwargs):
        Observable.__init__(self)
        BaseModel.__init__(self, **kwargs)
        self.poster = library.posters.get_default_poster_data()
        self.subtitle = None
        self.stop_download = False
        self.pause_state = const.NORMAL
        self.extension = 'avi'

    def __repr__(self):
        return self.title

    @async
    def load_poster(self):
        """Get poster from loader"""
        self.poster = yield proxy.posters.get_poster(title=self.title)

    @async
    def load_subtitle(self):
        """Get subtitles from loader"""
        subtitle = yield proxy.subtitles.get_subtitles(title=self.title)
        self.subtitle = Subtitle(**subtitle) if subtitle else None

    @property
    def file_name(self):
        try:
            return self._get_probably_name()
        except IndexError:
            return u'{}.{}'.format(self.title, self.extension)

    @property
    def path(self):
        return os.path.join(config.download_path, self.file_name)

    def remove_file(self):
        """Remove downloaded file"""
        try:
            name = self._get_probably_name()
        except IndexError:
            return
        full_path = os.path.join(os.path.dirname(self.path), name)
        os.unlink(full_path)

    def update(self, other):
        """Update from other model"""
        self.poster = other.poster
        self.subtitle = other.subtitle

    def _get_probably_name(self):
        """Get probably name"""
        pattern = '{}*'.format(os.path.join(
            config.download_path, self.title,
        ))
        return filter(
            lambda name: not name.endswith('.srt'), glob(pattern),
        )[0]

    @property
    def exists(self):
        """Is video downloaded"""
        try:
            return bool(self._get_probably_name())
        except IndexError:
            return False


class Subtitle(BaseModel):
    """Subtitle model"""

    def __init__(self, wait_for_file=False, **kwargs):
        super(Subtitle, self).__init__(
            wait_for_file=wait_for_file, **kwargs
        )

    def __repr__(self):
        return self.name

    @property
    def path(self):
        return os.path.join(config.download_path, u'{}.srt'.format(self.name))
