from ..lib.actors import Actor
from ..loaders import library


class SubtitlesActor(Actor):
    """Subtitles actor"""

    def run(self):
        library.import_all()
        super(SubtitlesActor, self).run()

    def get_subtitles(self, title):
        """Get subtitles for episodes"""
        return library.subtitles.get_subtitle_url(title)
