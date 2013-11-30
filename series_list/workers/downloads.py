import os
from PySide.QtCore import Signal, QObject, QTimer
from ..downloads.series import DownloadSeries
from ..downloads.subtitles import DownloadSubtitle
from ..models import SeriesEntry
from ..utils import ticked
from .. import const
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

    def _update_pause_state(self, entry, handler):
        """Update pause state"""
        if entry.pause_state == const.NEED_PAUSE:
            handler.pause()
            entry.pause_state = const.NORMAL
        elif entry.pause_state == const.NEED_RESUME:
            handler.resume()
            entry.pause_state = const.NORMAL

    @ticked
    def _download(self, entry, tick):
        """Get series"""
        handler = self.series.download(entry)
        entry.subtitle.series = entry
        if entry.subtitle.wait_for_file:
            entry.subtitle.downloaded = False
        else:
            self.subtitles.download(entry.subtitle)

        def _check_download():
            if (
                entry.subtitle.wait_for_file and
                not entry.subtitle.downloaded
                and os.path.exists(entry.path)
            ):
                self.subtitles.download(entry.subtitle)
            if entry.stop_download:
                handler.remove()
                entry.remove_file()
            self._update_pause_state(entry, handler)
            if handler.finished or entry.stop_download:
                self.downloaded.emit(entry, tick)
            else:
                QTimer.singleShot(100, _check_download)
            self.download_progress.emit(entry, handler.percent)
        _check_download()


class DownloadsWorkerThread(BaseWorkerThread):
    """Downloads worker"""
    worker = DownloadsWorker
