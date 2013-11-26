import sys
from PySide.QtCore import Slot
from PySide.QtGui import QApplication
from .workers import SeriesListWorkerThread, PosterWorkerThread
from .widgets.series_window import SeriesWindow
from .widgets.series_entry import SeriesEntryWidget
from .loaders.series import EZTVLoader
from .models import SeriesEntry


class SeriesListApp(QApplication):
    """Series list application"""

    def init(self, window):
        """Init application"""
        self.window = window
        self.eztv_loader = EZTVLoader()
        self._tick = 0
        self._init_workers()
        self._init_events()
        self._load_episodes()

    def _init_workers(self):
        """Init worker"""
        self.series_worker = SeriesListWorkerThread()
        self.series_worker.start()
        self.poster_worker = PosterWorkerThread()
        self.poster_worker.start()

    def _init_events(self):
        """Init events"""
        self.window.series_widget.need_more.connect(self._load_episodes)
        self.series_worker.receiver.received.connect(self._episode_received)

    @Slot(int, unicode)
    def _load_episodes(self, page=0, filters=None):
        """Load episodes"""
        self.series_worker.receiver.need_series.emit(page, filters, self._tick)

    @Slot(SeriesEntry, int)
    def _episode_received(self, episode, tick):
        """Episode received"""
        if tick == self._tick:
            entry = SeriesEntryWidget(episode)
            self.window.series_widget.add_entry(entry)
            self.need_poster(episode)

    def need_poster(self, episode):
        """Send need_poster to worker"""
        self.poster_worker.receiver.need_poster.emit(episode)


def main():
    app = SeriesListApp(sys.argv)
    window = SeriesWindow()
    window.show()
    app.init(window)
    app.exec_()


if __name__ == '__main__':
    main()
