from PySide.QtCore import QThread, Signal, QObject, Slot
from PySide.QtGui import QApplication
from ..models import SeriesEntry


class SubtitleWorker(QObject):
    """Subtitle worker"""
    need_subtitle = Signal(SeriesEntry, int)
    received = Signal(SeriesEntry, int)

    def __init__(self, *args, **kwargs):
        super(SubtitleWorker, self).__init__(*args, **kwargs)
        self.need_subtitle.connect(self._get_subtitle)

    @Slot(SeriesEntry, int)
    def _get_subtitle(self, episode, tick):
        """Get subtitle for episode"""
        if tick == QApplication.instance().tick:
            episode.load_subtitle()
            self.received.emit(episode, tick)


class SubtitleWorkerThread(QThread):
    """Poster worker"""

    def __init__(self):
        super(SubtitleWorkerThread, self).__init__()
        self.receiver = SubtitleWorker()
        self.receiver.moveToThread(self)
