from PySide.QtCore import Signal, Qt
from PySide.QtGui import QWidget
from ..lib.ui import WithUiMixin


class SeriesWidget(WithUiMixin, QWidget):
    """Series widget"""
    ui = 'series'
    need_more = Signal(int, unicode)

    def __init__(self, *args, **kwargs):
        super(SeriesWidget, self).__init__(*args, **kwargs)
        self._page = 0
        self._loading = False
        self._init_events()
        self._init_interface()

    def _init_interface(self):
        """Init user interface"""
        self.nothingFound.hide()
        self.somethingWrong.hide()

    def _init_events(self):
        """Init events"""
        self.scrollArea.verticalScrollBar()\
            .valueChanged.connect(self._on_scroll)

    def _show_loader(self):
        """Show loader"""
        self.nothingFound.hide()
        self.somethingWrong.hide()
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

    def something_wrong(self, message):
        """Handle faults"""
        self._hide_loader()
        self.nothingFound.hide()
        self.somethingWrong.setText(message)
        self.somethingWrong.show()
        self._update_alignment()

    def no_new_data(self):
        """No new data to add"""
        self._hide_loader()
        if self._page == 0:
            self.nothingFound.show()
        self._update_alignment()

    @property
    def series_layout(self):
        """Series layout"""
        return self.seriesContainer.layout()

    def add_entry(self, entry):
        """Add entry to series list"""
        self.series_layout.addWidget(entry)
        self._hide_loader()
        self.nothingFound.hide()
        self._update_alignment(is_add=True)

    def clear(self):
        """Clear series widget"""
        for index in range(self.series_layout.count()):
            self.series_layout.itemAt(index).widget().hide()
        self._page = 0
        self._update_alignment()
        self._show_loader()

    def _on_scroll(self, value):
        diff = self.scrollArea.verticalScrollBar().maximum() - value
        if diff == 0 and not self._loading:
            self._need_more()

    def _update_alignment(self, is_add=False):
        """Update alignment"""
        if self._page == 0 and not is_add:
            self.series_layout.setAlignment(Qt.AlignVCenter)
        else:
            self.series_layout.setAlignment(Qt.AlignTop)
