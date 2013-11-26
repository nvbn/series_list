from PySide.QtCore import QThread, Signal, QObject, Slot
from PySide.QtGui import QApplication
from ..models import SeriesEntry


class PosterWorker(QObject):
    """Poster worker"""
    need_poster = Signal(SeriesEntry, int)
    received = Signal(SeriesEntry, int)

    def __init__(self, *args, **kwargs):
        super(PosterWorker, self).__init__(*args, **kwargs)
        self.need_poster.connect(self._get_poster)

    @Slot(SeriesEntry, int)
    def _get_poster(self, episode, tick):
        """Get poster for episode"""
        if tick == QApplication.instance().tick:
            episode.load_poster()
            self.received.emit(episode, tick)


class PosterWorkerThread(QThread):
    """Poster worker"""

    def __init__(self):
        super(PosterWorkerThread, self).__init__()
        self.receiver = PosterWorker()
        self.receiver.moveToThread(self)
