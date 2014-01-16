from .. import library
from .base import SubtitlesLoader
from .subliminal_loader import SubliminalLoader
from .addicted import Addic7edLoader


def to_hashable(model):
    """Make model hashable"""
    return frozenset(model.items())


def composition(*loaders):
    """Create composition of loaders"""
    relations = {}

    def get_subtitle_url(self, name):
        for loader in loaders:
            result = loader().get_subtitle_url(name)
            if result:
                relations[to_hashable(result)] = loader
                return result

    def download(self, model):
        relations[to_hashable(model)]().download(model)

    return type(
        'Or'.join(loader.__name__ for loader in loaders),
        (SubtitlesLoader,), {
            'get_subtitle_url': get_subtitle_url,
            'download': download,
        },
    )

library.subtitles(composition(SubliminalLoader, Addic7edLoader))
