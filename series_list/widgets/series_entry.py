import subprocess
from PySide.QtCore import Slot
from PySide.QtGui import QWidget, QPixmap, QApplication
from ..interface.loader import WithUiMixin
from ..models import SeriesEntry


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
        self._set_poster_pixmap()
        QApplication.instance().poster_worker.receiver.received\
            .connect(self._maybe_poster_updated)

    @Slot(SeriesEntry)
    def _maybe_poster_updated(self, entry):
        """Maybe poster updated"""
        if entry == self.model:
            self._set_poster_pixmap()

    @Slot()
    def _set_poster_pixmap(self):
        """Get poster pixmap"""
        pixmap = QPixmap()
        pixmap.loadFromData(self.model.poster)
        self.poster.setPixmap(pixmap)

    def _init_events(self):
        """Init events and connect signals"""
        self.download.clicked.connect(self._download)

    @Slot()
    def _download(self):
        """Start downloading"""
        subprocess.Popen(['xdg-open', self.model.magnet])
