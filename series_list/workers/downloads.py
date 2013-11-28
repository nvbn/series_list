from PySide.QtCore import Signal, QObject, Slot, QTimer
from ..downloads.series import DownloadSeries
from ..downloads.subtitles import DownloadSubtitle
from ..models import SeriesEntry
from ..utils import ticked
from .base import BaseWorkerThread


class DownloadsWorker(QObject):
    """Series list worker"""
    need_download = Signal(SeriesEntry, int)
    downloaded = Signal(SeriesEntry, int)
    download_progress = Signal(SeriesEntry, float)

    def __init__(self, *args, **kwargs):
        super(DownloadsWorker, self).__init__(*args, **kwargs)
        self.subtitles = DownloadSubtitle()
        self.series = DownloadSeries()
        self.need_download.connect(self._download)

    @Slot(int, unicode, int)
    @ticked
    def _download(self, entry, tick):
        """Get series"""
        handler = self.series.download(entry)
        self.subtitles.download(entry.subtitle)

        @Slot()
        def _check_download():
            if entry.stop_download:
                handler.remove()
                entry.remove_file()
            if handler.finished or entry.stop_download:
                self.downloaded.emit(entry, tick)
            else:
                QTimer.singleShot(100, _check_download)
            self.download_progress.emit(entry, handler.percent)
        _check_download()


class DownloadsWorkerThread(BaseWorkerThread):
    """Downloads worker"""
    worker = DownloadsWorker
