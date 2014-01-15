from ..lib.actors import Actor
from ..loaders import library


class PostersActor(Actor):
    """Posters actor"""

    def run(self):
        library.import_all()
        super(PostersActor, self).run()

    def set_poster(self, episode):
        """Get poster for episodes"""
        episode.load_poster()
        return episode
