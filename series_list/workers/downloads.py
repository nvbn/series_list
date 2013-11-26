from PySide.QtCore import Signal, QObject, Slot
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
        self.series.download(entry)
        self.subtitles.download(entry.subtitle)
        self.downloaded.emit(entry, tick)


class DownloadsWorkerThread(BaseWorkerThread):
    """Downloads worker"""
    worker = DownloadsWorker
