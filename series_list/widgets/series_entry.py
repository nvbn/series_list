from PySide.QtGui import QWidget
from ..interface.loader import WithUiMixin


class SeriesEntryWidget(WithUiMixin, QWidget):
    """Series entry widget"""
    ui = 'series_entry'
