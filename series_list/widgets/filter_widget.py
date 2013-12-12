from PySide.QtCore import Signal
from PySide.QtGui import QWidget
from ..interface.loader import WithUiMixin


class FilterWidget(WithUiMixin, QWidget):
    """Filter widget"""
    ui = 'filter'
    icons = {
        'filterButton': ('view-refresh', 'series-list-refresh'),
    }
    filter_changed = Signal(unicode)

    def __init__(self, *args, **kwargs):
        super(FilterWidget, self).__init__(*args, **kwargs)
        self._init_events()
        self._prevs = []
        self._nexts = []
        self._current = ''

    def _init_events(self):
        """Init events and connect signals"""
        self.filterButton.clicked.connect(self._update_filter)
        self.filterEdit.textChanged.connect(self._update_filter)
        self.filterEdit.editingFinished.connect(self._update_history)

    def set_window_events(self, window):
        """Set window events"""
        window.need_previous_query.connect(self._previous_query)
        window.need_next_query.connect(self._next_query)

    def _update_filter(self):
        """Update filter"""
        value = self.filterEdit.text()
        self.filter_changed.emit(value)

    def _previous_query(self):
        """Update with previous query"""
        if len(self._prevs):
            self._nexts.insert(0, self._current)
            query = self._prevs.pop(-1)
            self._current = query
            self.filterEdit.setText(query)

    def _next_query(self):
        """Update with next query"""
        if len(self._nexts):
            query = self._nexts.pop()
            self._prevs.append(self._current)
            self._current = query
            self.filterEdit.setText(query)

    def _update_history(self):
        """Update query history"""
        current = self.filterEdit.text()
        if self._current != current:
            self._prevs.append(self._current)
            self._current = current
            self._nexts = []
