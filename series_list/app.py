import sys
from PySide.QtCore import Slot, Signal
from PySide.QtGui import QApplication
from .workers import SeriesListWorkerThread, PosterWorkerThread, SubtitleWorkerThread
from .widgets.series_window import SeriesWindow
from .widgets.series_entry import SeriesEntryWidget
from .loaders.series import EZTVLoader
from .models import SeriesEntry


class SeriesListApp(QApplication):
    """Series list application"""
    poster_received = Signal(SeriesEntry)
    subtitle_received = Signal(SeriesEntry)

    def init(self, window):
        """Init application"""
        self.window = window
        self.eztv_loader = EZTVLoader()
        self._tick = 0
        self._filter = ''
        self._init_workers()
        self._init_events()
        self._load_episodes()

    def _init_workers(self):
        """Init worker"""
        self.series_worker = SeriesListWorkerThread()
        self.series_worker.start()
        self.poster_worker = PosterWorkerThread()
        self.poster_worker.start()
        self.subtitle_worker = SubtitleWorkerThread()
        self.subtitle_worker.start()

    def _init_events(self):
        """Init events"""
        self.window.series_widget.need_more.connect(self._load_episodes)
        self.series_worker.receiver.received.connect(self._episode_received)
        self.window.filter_widget.filter_changed.connect(self._filter_changed)
        self.poster_worker.receiver.received.connect(self._poster_received)
        self.subtitle_worker.receiver.received.connect(self._subtitle_received)

    @Slot(int)
    def _load_episodes(self, page=0):
        """Load episodes"""
        self.series_worker.receiver.need_series.emit(
            page, self._filter, self._tick,
        )

    @Slot(SeriesEntry, int)
    def _episode_received(self, episode, tick):
        """Episode received"""
        if tick == self._tick:
            entry = SeriesEntryWidget(episode)
            self.window.series_widget.add_entry(entry)
            self.need_poster(episode)
            self.need_subtitle(episode)

    @Slot(SeriesEntry, int)
    def _poster_received(self, episode, tick):
        """Poster received"""
        if tick == self._tick:
            self.poster_received.emit(episode)

    @Slot(SeriesEntry, int)
    def _subtitle_received(self, episode, tick):
        """Subtitle received"""
        if tick == self._tick:
            self.subtitle_received.emit(episode)

    def need_poster(self, episode):
        """Send need_poster to worker"""
        self.poster_worker.receiver.need_poster.emit(episode, self._tick)

    def need_subtitle(self, episode):
        """Send need_subtitle to worker"""
        self.subtitle_worker.receiver.need_subtitle.emit(episode, self._tick)

    @Slot(unicode)
    def _filter_changed(self, value):
        """Filter changed"""
        self.window.series_widget.clear()
        self._tick += 1
        self._filter = value
        self._load_episodes()


def main():
    app = SeriesListApp(sys.argv)
    window = SeriesWindow()
    window.show()
    app.init(window)
    app.exec_()


if __name__ == '__main__':
    main()
