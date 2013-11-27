from PySide.QtCore import Signal, QObject, Slot, QRunnable, QThreadPool
from ..models import SeriesEntry
from ..utils import ticked
from .base import BaseWorkerThread


class SubtitleReceiver(QRunnable):
    """Subtitle receiver"""

    def __init__(self, episode, on_finish):
        super(SubtitleReceiver, self).__init__()
        self._on_finish = on_finish
        self._episode = episode

    def run(self):
        self._episode.load_subtitle()
        self._on_finish()


class SubtitleWorker(QObject):
    """Subtitle worker"""
    need_subtitle = Signal(SeriesEntry, int)
    received = Signal(SeriesEntry, int)

    def __init__(self, *args, **kwargs):
        super(SubtitleWorker, self).__init__(*args, **kwargs)
        self.need_subtitle.connect(self._get_subtitle)
        self.pool = QThreadPool(self)
        self.pool.setMaxThreadCount(5)

    @Slot(SeriesEntry, int)
    @ticked
    def _get_subtitle(self, episode, tick):
        """Get subtitle for episode"""
        runnable = SubtitleReceiver(
            episode, lambda: self.received.emit(episode, tick),
        )
        self.pool.start(runnable)


class SubtitleWorkerThread(BaseWorkerThread):
    """Poster worker"""
    worker = SubtitleWorker
