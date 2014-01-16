from ..lib.green import GreenActor
from ..loaders import library
from .base import WithLibraryMixin


class EpisodeActor(WithLibraryMixin, GreenActor):
    """Episode actor"""
    max_wait = 1

    def get_episodes(self, page, filters):
        """Get episodes"""
        return library.series.get_series(page, filters)
