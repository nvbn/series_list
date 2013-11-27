from PySide.QtCore import Signal, Slot
from PySide.QtGui import QWidget
from ..interface.loader import WithUiMixin


class SeriesWidget(WithUiMixin, QWidget):
    """Series widget"""
    ui = 'series'
    need_more = Signal(int, unicode)

    def __init__(self, *args, **kwargs):
        super(SeriesWidget, self).__init__(*args, **kwargs)
        self._page = 0
        self._init_events()

    def _init_events(self):
        """Init events"""
        self.moreButton.clicked.connect(self._need_more)

    @Slot()
    def _need_more(self):
        """Need more entries"""
        self._page += 1
        self.need_more.emit(self._page, None)

    @property
    def series_layout(self):
        """Series layout"""
        return self.seriesContainer.layout()

    def add_entry(self, entry):
        """Add entry to series list"""
        self.series_layout.addWidget(entry)
        self.loading.hide()

    def clear(self):
        """Clear series widget"""
        for index in range(self.series_layout.count()):
            self.series_layout.itemAt(index).widget().hide()
        self._page = 0
        self.loading.show()
