from PySide.QtGui import QWidget
from ..interface.loader import WithUiMixin


class FilterWidget(WithUiMixin, QWidget):
    """Filter widget"""
    ui = 'filter'
