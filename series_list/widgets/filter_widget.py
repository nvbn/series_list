from PySide.QtCore import Signal, Slot
from PySide.QtGui import QWidget
from ..interface.loader import WithUiMixin


class FilterWidget(WithUiMixin, QWidget):
    """Filter widget"""
    ui = 'filter'
    filter_changed = Signal(unicode)

    def __init__(self, *args, **kwargs):
        super(FilterWidget, self).__init__(*args, **kwargs)
        self._init_events()

    def _init_events(self):
        """Init events and connect signals"""
        self.filterButton.clicked.connect(self._update_filter)
        self.filterEdit.returnPressed.connect(self._update_filter)

    @Slot()
    def _update_filter(self):
        """Update filter"""
        value = self.filterEdit.text()
        self.filter_changed.emit(value)
