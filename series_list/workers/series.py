import traceback
from PySide.QtCore import Signal, QObject
from ..loaders import library
from ..models import SeriesEntry
from ..utils import ticked
from .base import BaseWorkerThread


class SeriesListWorker(QObject):
    """Series list worker"""
    need_series = Signal(int, unicode, int)
    received = Signal(SeriesEntry, int)
    no_new_data = Signal(int)
    something_wrong = Signal(unicode, int)

    def __init__(self, *args, **kwargs):
        super(SeriesListWorker, self).__init__(*args, **kwargs)
        self.need_series.connect(self._get_series)

    @ticked
    def _get_series(self, page, filters, tick):
        """Get series"""
        try:
            series = library.series.get_series(page, filters)
        except Exception as e:
            print e
            traceback.print_exc()
            self.something_wrong.emit(library.series.error_message, tick)
            return

        if series:
            for episode in series:
                self.received.emit(episode, tick)
        else:
            self.no_new_data.emit(tick)


class SeriesListWorkerThread(BaseWorkerThread):
    """Series list worker"""
    worker = SeriesListWorker
