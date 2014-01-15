from .procs.fetcher import FetcherActor
from .procs.gui import GuiActor


def main():
    """Start app procs"""
    fetcher_p = FetcherActor('fetcher')
    gui = GuiActor('gui')
    gui.start()
    fetcher_p.start()
    gui.join()
    gui.terminate()
    fetcher_p.terminate()


if __name__ == '__main__':
    main()
