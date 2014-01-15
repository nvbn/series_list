from ..lib.green import GreenActor
from ..loaders import library


class EpisodeActor(GreenActor):
    """Episode actor"""
    max_wait = 1

    def run(self):
        library.import_all()
        super(EpisodeActor, self).run()

    def get_episodes(self, page, filters):
        """Get episodes"""
        return library.series.get_series(page, filters)
