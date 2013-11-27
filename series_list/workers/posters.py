from PySide.QtCore import Signal, QObject, Slot, QThreadPool, QRunnable
from ..models import SeriesEntry
from ..utils import ticked
from .base import BaseWorkerThread


class PosterReceiver(QRunnable):
    """Poster receiver"""

    def __init__(self, episode, on_finish):
        super(PosterReceiver, self).__init__()
        self._on_finish = on_finish
        self._episode = episode

    def run(self):
        self._episode.load_poster()
        self._on_finish()


class PosterWorker(QObject):
    """Poster worker"""
    need_poster = Signal(SeriesEntry, int)
    received = Signal(SeriesEntry, int)

    def __init__(self, *args, **kwargs):
        super(PosterWorker, self).__init__(*args, **kwargs)
        self.need_poster.connect(self._get_poster)
        self.pool = QThreadPool(self)
        self.pool.setMaxThreadCount(5)

    @Slot(SeriesEntry, int)
    @ticked
    def _get_poster(self, episode, tick):
        """Get poster for episode"""
        runnable = PosterReceiver(
            episode, lambda: self.received.emit(episode, tick),
        )
        self.pool.start(runnable)


class PosterWorkerThread(BaseWorkerThread):
    """Poster worker"""
    worker = PosterWorker
