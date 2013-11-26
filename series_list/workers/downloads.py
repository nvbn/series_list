import os
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

    def __init__(self, *args, **kwargs):
        super(DownloadsWorker, self).__init__(*args, **kwargs)
        self.subtitles = DownloadSubtitle()
        self.series = DownloadSeries()
        self.need_download.connect(self._download)

    @Slot(int, unicode, int)
    @ticked
    def _download(self, entry, tick):
        """Get series"""
        proc = self.series.download(entry)
        self.subtitles.download(entry.subtitle)

        @Slot()
        def _check_download():
            if entry.stop_download:
                proc.kill()
                if os.path.exists(entry.path):
                    os.unlink(entry.path)
            if proc.poll() is not None or entry.stop_download:
                self.downloaded.emit(entry, tick)
            else:
                QTimer.singleShot(500, _check_download)
        _check_download()


class DownloadsWorkerThread(BaseWorkerThread):
    """Downloads worker"""
    worker = DownloadsWorker
