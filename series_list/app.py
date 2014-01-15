from .lib.actors import actors
from .procs.gui import GuiActor
from .procs.episodes import EpisodeActor
from .procs.subtitles import SubtitlesActor
from .procs.posters import PostersActor


def main():
    """Start app procs"""
    gui = GuiActor('gui')
    episodes = EpisodeActor('episodes')
    subtitles = SubtitlesActor('subtitles')
    posters = PostersActor('posters')
    gui.start()
    episodes.start()
    subtitles.start()
    posters.start()
    gui.join()
    for actor in actors.values():
        actor.terminate()


if __name__ == '__main__':
    main()
