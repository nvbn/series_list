from PySide.QtCore import Signal, QObject, Slot
from ..loaders import library
from ..models import SeriesEntry
from ..utils import ticked
from .base import BaseWorkerThread


class SeriesListWorker(QObject):
    """Series list worker"""
    need_series = Signal(int, unicode, int)
    received = Signal(SeriesEntry, int)

    def __init__(self, *args, **kwargs):
        super(SeriesListWorker, self).__init__(*args, **kwargs)
        self.need_series.connect(self._get_series)

    @Slot(int, unicode, int)
    @ticked
    def _get_series(self, page, filters, tick):
        """Get series"""
        for episode in library.series.get_series(page, filters):
            self.received.emit(episode, tick)


class SeriesListWorkerThread(BaseWorkerThread):
    """Series list worker"""
    worker = SeriesListWorker
