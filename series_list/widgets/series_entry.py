import subprocess
from PySide.QtCore import Slot
from PySide.QtGui import QWidget
from ..interface.loader import WithUiMixin


class SeriesEntryWidget(WithUiMixin, QWidget):
    """Series entry widget"""
    ui = 'series_entry'

    def __init__(self, model, *args, **kwargs):
        super(SeriesEntryWidget, self).__init__(*args, **kwargs)
        self._set_model(model)
        self._init_events()

    def _set_model(self, model):
        """Ste data from model to entry"""
        self.model = model
        self.title.setText(model.title)

    def _init_events(self):
        """Init events and connect signals"""
        self.download.clicked.connect(self._download)

    @Slot()
    def _download(self):
        """Start downloading"""
        subprocess.Popen(['xdg-open', self.model.magnet])
