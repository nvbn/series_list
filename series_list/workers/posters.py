from PySide.QtCore import Signal, QObject, Slot
from ..models import SeriesEntry
from ..utils import ticked
from .base import BaseWorkerThread


class PosterWorker(QObject):
    """Poster worker"""
    need_poster = Signal(SeriesEntry, int)
    received = Signal(SeriesEntry, int)

    def __init__(self, *args, **kwargs):
        super(PosterWorker, self).__init__(*args, **kwargs)
        self.need_poster.connect(self._get_poster)

    @Slot(SeriesEntry, int)
    @ticked
    def _get_poster(self, episode, tick):
        """Get poster for episode"""
        episode.load_poster()
        self.received.emit(episode, tick)


class PosterWorkerThread(BaseWorkerThread):
    """Poster worker"""
    worker = PosterWorker
