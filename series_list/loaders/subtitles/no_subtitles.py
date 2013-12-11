from ...models import Subtitle
from .. import library
from .base import SubtitlesLoader


@library.subtitles
class NoSubtitlesLoader(SubtitlesLoader):
    """For downloading without subtitles"""

    def get_subtitle_url(self, name):
        """Always return ok"""
        return Subtitle(
            name=name,
            wait_for_file=True,
        )

    def download(self, model):
        """No download subtitles"""
