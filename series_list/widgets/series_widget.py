from PySide.QtGui import QWidget
from ..interface.loader import WithUiMixin


class SeriesWidget(WithUiMixin, QWidget):
    """Series widget"""
    ui = 'series'
