from PySide.QtGui import QWidget
from ..interface.loader import WithUiMixin


class DownloadEntryWidget(WithUiMixin, QWidget):
    """Download entry widget"""
    ui = 'download_entry'
