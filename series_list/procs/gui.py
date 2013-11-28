from Queue import Empty
import sys
import subprocess
from PySide.QtCore import Slot, Signal, QTimer, QSettings
from PySide.QtGui import QApplication
from ..workers.downloads import DownloadsWorkerThread
from ..workers.series import SeriesListWorkerThread
from ..widgets.series_window import SeriesWindow
from ..widgets.series_entry import SeriesEntryWidget
from ..loaders import library
from ..models import SeriesEntry
from ..utils import ticked
from ..settings import config


class SeriesListApp(QApplication):
    """Series list application"""
    downloaded = Signal(SeriesEntry)
    download_progress = Signal(SeriesEntry, float)
    entry_updated = Signal(SeriesEntry)

    def init(self, window):
        """Init application"""
        self.window = window
        self._tick = 0
        self._filter = ''
        self._init_workers()
        self._init_events()
        self._load_episodes()

    def _init_workers(self):
        """Init worker"""
        self.series_worker = SeriesListWorkerThread()
        self.series_worker.start()
        self.downloads_worker = DownloadsWorkerThread()
        self.downloads_worker.start()

    def _init_events(self):
        """Init events"""
        self.window.series_widget.need_more.connect(self._load_episodes)
        self.series_worker.received.connect(self._episode_received)
        self.window.filter_widget.filter_changed.connect(self._filter_changed)
        self.downloads_worker.downloaded.connect(self._downloaded)
        self.downloads_worker.download_progress.connect(self._download_progress)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_queue)
        self.timer.start(50)

    @Slot(int)
    def _load_episodes(self, page=0):
        """Load episodes"""
        if page > 0 and self._filter:
            self.window.series_widget._hide_loader()
            return

        self.series_worker.need_series.emit(
            page, self._filter, self.tick,
        )

    @Slot(SeriesEntry, int)
    @ticked
    def _episode_received(self, episode, tick):
        """Episode received"""
        entry = SeriesEntryWidget.get_or_create(episode)
        self.window.series_widget.add_entry(entry)
        self.out_queue.put((episode, self.tick))

    @Slot(SeriesEntry, int)
    def _downloaded(self, episode, tick):
        """Downloaded"""
        self.downloaded.emit(episode)

    @Slot(SeriesEntry, float)
    def _download_progress(self, episode, value):
        """Download progress"""
        self.download_progress.emit(episode, value)

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

    @ticked
    def _update_received(self, episode, tick):
        """Update received"""
        self.entry_updated.emit(episode)

    def check_queue(self):
        while True:
            try:
                data = self.in_queue.get_nowait()
                self._update_received(*data)
            except Empty:
                break

    @property
    def tick(self):
        return self._tick

    @tick.setter
    def tick(self, value):
        self._tick = value
        self.shared_tick.value = value


def gui_proc(in_queue, out_queue, tick):
    """Gut process"""
    library.import_all()
    app = SeriesListApp(sys.argv)
    app.in_queue = in_queue
    app.out_queue = out_queue
    app.shared_tick = tick
    subprocess.call(['mkdir', '-p', config.download_path])
    window = SeriesWindow()
    window.show()
    app.init(window)
    app.exec_()
