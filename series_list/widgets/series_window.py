from PySide.QtGui import QMainWindow, QVBoxLayout, QWidget
from .filter_widget import FilterWidget
from .series_widget import SeriesWidget
from .downloads_widget import DownloadsWidget


class SeriesWindow(QMainWindow):
    """Series window"""

    def __init__(self, *args, **kwargs):
        super(SeriesWindow, self).__init__(*args, **kwargs)
        self._init_interface()

    def _init_interface(self):
        """Init window interface"""
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.filter_widget = FilterWidget()
        self.series_widget = SeriesWidget()
        self.downloads_widget = DownloadsWidget()
        layout.addWidget(self.filter_widget)
        layout.addWidget(self.series_widget)
        layout.addWidget(self.downloads_widget)
        self.setCentralWidget(widget)
