from ..lib.green import GreenActor
from ..loaders import library
from .base import WithLibraryMixin


class SubtitlesActor(WithLibraryMixin, GreenActor):
    """Subtitles actor"""

    def get_subtitles(self, title):
        """Get subtitles for episodes"""
        return library.subtitles.get_subtitle_url(title)
