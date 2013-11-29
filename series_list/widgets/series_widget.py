from PySide.QtCore import Signal
from PySide.QtGui import QWidget
from ..interface.loader import WithUiMixin


class SeriesWidget(WithUiMixin, QWidget):
    """Series widget"""
    ui = 'series'
    need_more = Signal(int, unicode)

    def __init__(self, *args, **kwargs):
        super(SeriesWidget, self).__init__(*args, **kwargs)
        self._page = 0
        self._loading = False
        self._init_events()

    def _init_events(self):
        """Init events"""
        self.scrollArea.verticalScrollBar()\
            .valueChanged.connect(self._on_scroll)

    def _show_loader(self):
        """Show loader"""
        self._loading = True
        self.series_layout.removeWidget(self.loading)
        self.series_layout.addWidget(self.loading)
        self.loading.show()

    def _hide_loader(self):
        """Hide loader"""
        self._loading = False
        self.loading.hide()

    def _need_more(self):
        """Need more entries"""
        self._show_loader()
        self._page += 1
        self.need_more.emit(self._page, None)

    @property
    def series_layout(self):
        """Series layout"""
        return self.seriesContainer.layout()

    def add_entry(self, entry):
        """Add entry to series list"""
        self.series_layout.addWidget(entry)
        self._hide_loader()

    def clear(self):
        """Clear series widget"""
        for index in range(self.series_layout.count()):
            self.series_layout.itemAt(index).widget().hide()
        self._page = 0
        self._show_loader()

    def _on_scroll(self, value):
        diff = self.scrollArea.verticalScrollBar().maximum() - value
        if diff == 0 and not self._loading:
            self._need_more()
