from .procs.fetcher import FetcherActor
from .procs.gui import GuiActor
from .procs.episodes import EpisodeActor


def main():
    """Start app procs"""
    fetcher_p = FetcherActor('fetcher')
    gui = GuiActor('gui')
    episodes = EpisodeActor('episodes')
    gui.start()
    fetcher_p.start()
    episodes.start()
    gui.join()
    gui.terminate()
    fetcher_p.terminate()


if __name__ == '__main__':
    main()
