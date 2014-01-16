from .. import library
from .base import SubtitlesLoader
from .subliminal_loader import SubliminalLoader
from .addicted import Addic7edLoader


def composition(*loaders):
    """Create composition of loaders"""
    def get_subtitle_url(self, name):
        for loader in loaders:
            result = loader().get_subtitle_url(name)
            if result:
                result['loader_name'] = loader.__name__
                return result

    def download(self, model):
        for loader in loaders:
            if loader.__name__ == model.loader_name:
                loader().download(model)

    return type(
        'Or'.join(loader.__name__ for loader in loaders),
        (SubtitlesLoader,), {
            'get_subtitle_url': get_subtitle_url,
            'download': download,
        },
    )

library.subtitles(composition(SubliminalLoader, Addic7edLoader))
