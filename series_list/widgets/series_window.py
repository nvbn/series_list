import os
import subprocess
from PySide.QtCore import Signal, Qt
from PySide.QtGui import QMainWindow, QVBoxLayout, QWidget, QIcon
from .. import const
from ..settings import config
from ..lib.ui import WithUiMixin
from .filter_widget import FilterWidget
from .series_widget import SeriesWidget
from .settings_dialog import SettingsDialog


class SeriesWindow(WithUiMixin, QMainWindow):
    """Series window"""
    ui = 'window'
    need_previous_query = Signal()
    need_next_query = Signal()

    def __init__(self, *args, **kwargs):
        super(SeriesWindow, self).__init__(*args, **kwargs)
        self._settings_dialog = None
        self._init_window()
        self._init_interface()
        self._init_events()

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

    def _init_events(self):
        """Init events"""
        self.actionExit.triggered.connect(self.close)
        self.actionSettings.triggered.connect(self._show_settings)
        self.actionOpenDownloads.triggered.connect(self._open_downloads)
        self.filter_widget.set_window_events(self)

    def _show_settings(self):
        """Show settings dialog"""
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()

    def mouseReleaseEvent(self, event):
        """Process mouse back/forward gestures"""
        button = event.button()
        if button == Qt.MouseButton.XButton1:
            self.need_previous_query.emit()
            event.accept()
        elif button == Qt.MouseButton.XButton2:
            self.need_next_query.emit()
            event.accept()

    def _open_downloads(self):
        """Open downloads path"""
        subprocess.Popen(['xdg-open', config.download_path])
