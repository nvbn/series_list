import sys
import subprocess
from PySide.QtCore import Slot, Signal
from PySide.QtGui import QApplication
from .workers.posters import PosterWorkerThread
from .workers.series import SeriesListWorkerThread
from .workers.subtitles import SubtitleWorkerThread
from .workers.downloads import DownloadsWorkerThread
from .widgets.series_window import SeriesWindow
from .widgets.series_entry import SeriesEntryWidget
from .loaders.series import EZTVLoader
from .models import SeriesEntry
from .utils import ticked
from . import const


class SeriesListApp(QApplication):
    """Series list application"""
    poster_received = Signal(SeriesEntry)
    subtitle_received = Signal(SeriesEntry)
    downloaded = Signal(SeriesEntry)
    download_progress = Signal(SeriesEntry, float)

    def init(self, window):
        """Init application"""
        self.window = window
        self.eztv_loader = EZTVLoader()
        self.tick = 0
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
        self.downloads_worker = DownloadsWorkerThread()
        self.downloads_worker.start()

    def _init_events(self):
        """Init events"""
        self.window.series_widget.need_more.connect(self._load_episodes)
        self.series_worker.received.connect(self._episode_received)
        self.window.filter_widget.filter_changed.connect(self._filter_changed)
        self.poster_worker.received.connect(self._poster_received)
        self.subtitle_worker.received.connect(self._subtitle_received)
        self.downloads_worker.downloaded.connect(self._downloaded)
        self.downloads_worker.download_progress.connect(self._download_progress)

    @Slot(int)
    def _load_episodes(self, page=0):
        """Load episodes"""
        self.series_worker.need_series.emit(
            page, self._filter, self.tick,
        )

    @Slot(SeriesEntry, int)
    @ticked
    def _episode_received(self, episode, tick):
        """Episode received"""
        entry = SeriesEntryWidget.get_or_create(episode)
        self.window.series_widget.add_entry(entry)
        self.need_poster(episode)
        self.need_subtitle(episode)

    @Slot(SeriesEntry, int)
    @ticked
    def _poster_received(self, episode, tick):
        """Poster received"""
        self.poster_received.emit(episode)

    @Slot(SeriesEntry, int)
    @ticked
    def _subtitle_received(self, episode, tick):
        """Subtitle received"""
        self.subtitle_received.emit(episode)

    @Slot(SeriesEntry, int)
    def _downloaded(self, episode, tick):
        """Downloaded"""
        self.downloaded.emit(episode)

    @Slot(SeriesEntry, float)
    def _download_progress(self, episode, value):
        """Download progress"""
        self.download_progress.emit(episode, value)

    def need_poster(self, episode):
        """Send need_poster to worker"""
        self.poster_worker.need_poster.emit(episode, self.tick)

    def need_subtitle(self, episode):
        """Send need_subtitle to worker"""
        self.subtitle_worker.need_subtitle.emit(episode, self.tick)

    def need_download(self, episode):
        """Send need_subtitle to worker"""
        self.downloads_worker.need_download.emit(episode, self.tick)

    @Slot(unicode)
    def _filter_changed(self, value):
        """Filter changed"""
        self.window.series_widget.clear()
        self.tick += 1
        self._filter = value
        self._load_episodes()


def main():
    subprocess.call(['mkdir', '-p', const.DOWNLOAD_PATH])
    app = SeriesListApp(sys.argv)
    window = SeriesWindow()
    window.show()
    app.init(window)
    app.exec_()


if __name__ == '__main__':
    main()
