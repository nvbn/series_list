from ..lib.actors import Actor
from ..loaders import library


class SubtitlesActor(Actor):
    """Subtitles actor"""

    def run(self):
        library.import_all()
        super(SubtitlesActor, self).run()

    def set_subtitles(self, episode):
        """Get subtitles for episodes"""
        episode.load_subtitle()
        return episode
