from PySide.QtGui import QWidget
from ..interface.loader import WithUiMixin


class SeriesWidget(WithUiMixin, QWidget):
    """Series widget"""
    ui = 'series'

    @property
    def series_layout(self):
        """Series layout"""
        return self.seriesContainer.layout()

    def add_entry(self, entry):
        """Add entry to series list"""
        self.series_layout.addWidget(entry)

    def clear(self):
        """Clear series widget"""
        for index in range(self.series_layout.count()):
            self.series_layout.itemAt(index).widget().deleteLater()
