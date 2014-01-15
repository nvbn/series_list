from ..lib.actors import Actor
from ..loaders import library


class EpisodeActor(Actor):
    """Episode actor"""

    def run(self):
        library.import_all()
        super(EpisodeActor, self).run()

    def get_episodes(self, page, filters):
        """Get episodes"""
        return library.series.get_series(page, filters)
