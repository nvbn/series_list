from ..lib.green import GreenActor
from ..loaders import library
from .base import WithLibraryMixin


class PostersActor(WithLibraryMixin, GreenActor):
    """Posters actor"""

    def get_poster(self, title):
        """Get poster for episodes"""
        return library.posters.get_poster_data(title)
