import os
from PySide.QtGui import QMainWindow, QVBoxLayout, QWidget, QIcon
from .. import const
from .filter_widget import FilterWidget
from .series_widget import SeriesWidget


class SeriesWindow(QMainWindow):
    """Series window"""

    def __init__(self, *args, **kwargs):
        super(SeriesWindow, self).__init__(*args, **kwargs)
        self._init_window()
        self._init_interface()

    def _init_window(self):
        """Init window attributes"""
        self.setWindowTitle('Series list')
        if os.path.exists(const.ICON_PATH):
            icon = QIcon()
            icon.addFile(const.ICON_PATH)
        else:
            icon = QIcon.fromTheme('series_list_icon')
        self.setWindowIcon(icon)

    def _init_interface(self):
        """Init window interface"""
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.filter_widget = FilterWidget()
        self.series_widget = SeriesWidget()
        layout.addWidget(self.filter_widget)
        layout.addWidget(self.series_widget)
        self.setCentralWidget(widget)
        widget.setContentsMargins(0, 0, 0, 0)
