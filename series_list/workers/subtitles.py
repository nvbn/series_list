from PySide.QtCore import Signal, QObject, Slot
from PySide.QtGui import QApplication
from ..models import SeriesEntry
from ..utils import ticked
from .base import BaseWorkerThread


class SubtitleWorker(QObject):
    """Subtitle worker"""
    need_subtitle = Signal(SeriesEntry, int)
    received = Signal(SeriesEntry, int)

    def __init__(self, *args, **kwargs):
        super(SubtitleWorker, self).__init__(*args, **kwargs)
        self.need_subtitle.connect(self._get_subtitle)

    @Slot(SeriesEntry, int)
    @ticked
    def _get_subtitle(self, episode, tick):
        """Get subtitle for episode"""
        episode.load_subtitle()
        self.received.emit(episode, tick)


class SubtitleWorkerThread(BaseWorkerThread):
    """Poster worker"""
    worker = SubtitleWorker
