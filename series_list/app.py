import multiprocessing
from .procs.fetcher import fetcher_proc
from .procs.gui import gui_proc


def main():
    """Start app procs"""
    fetcher_in = multiprocessing.Queue()
    gui_in = multiprocessing.Queue()
    tick = multiprocessing.Value('i')
    tick.value = 0
    gui = multiprocessing.Process(target=gui_proc, args=(
        gui_in, fetcher_in, tick,
    ))
    fetcher_p = multiprocessing.Process(target=fetcher_proc, args=(
        fetcher_in, gui_in, tick,
    ))
    gui.start()
    fetcher_p.start()
    gui.join()
    gui.terminate()
    fetcher_p.terminate()


if __name__ == '__main__':
    main()
