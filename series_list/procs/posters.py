from ..lib.actors import Actor
from ..loaders import library


class PostersActor(Actor):
    """Posters actor"""

    def run(self):
        library.import_all()
        super(PostersActor, self).run()

    def get_poster(self, title):
        """Get poster for episodes"""
        return library.posters.get_poster_data(title)
