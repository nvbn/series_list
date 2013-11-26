from PySide.QtCore import QThread, Signal, QObject, Slot
from ..loaders.series import EZTVLoader
from ..models import SeriesEntry


class SeriesListWorker(QObject):
    """Series list worker"""
    need_series = Signal(int, unicode, int)
    received = Signal(SeriesEntry, int)

    def __init__(self, *args, **kwargs):
        super(SeriesListWorker, self).__init__(*args, **kwargs)
        self.loader = EZTVLoader()
        self.need_series.connect(self._get_series)

    @Slot(int, unicode, int)
    def _get_series(self, page, filters, tick):
        """Get series"""
        for episode in self.loader.get_series(page, filters):
            self.received.emit(episode, tick)


class SeriesListWorkerThread(QThread):
    """Series list worker"""

    def __init__(self):
        super(SeriesListWorkerThread, self).__init__()
        self.receiver = SeriesListWorker()
        self.receiver.moveToThread(self)
