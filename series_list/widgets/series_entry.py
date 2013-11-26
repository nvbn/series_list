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
        self._update_subtitle()
        QApplication.instance().poster_received.connect(self._maybe_poster_updated)
        QApplication.instance().subtitle_received.connect(self._maybe_subtitle_updated)

    @Slot(SeriesEntry)
    def _maybe_poster_updated(self, entry):
        """Maybe poster updated"""
        if entry == self.model:
            self._set_poster_pixmap()

    @Slot(SeriesEntry)
    def _maybe_subtitle_updated(self, entry):
        """Maybe subtitle updated"""
        if entry == self.model:
            self._update_subtitle()

    @Slot()
    def _set_poster_pixmap(self):
        """Get poster pixmap"""
        pixmap = QPixmap()
        pixmap.loadFromData(self.model.poster)
        self.poster.setPixmap(pixmap)

    @Slot()
    def _update_subtitle(self):
        """Update subtitle status"""
        if self.model.subtitle:
            self.subtitles.setEnabled(True)
        else:
            self.subtitles.setEnabled(False)

    def _init_events(self):
        """Init events and connect signals"""
        self.download.clicked.connect(self._download)
        self.subtitles.clicked.connect(self._download_subtitles)

    @Slot()
    def _download(self):
        """Start downloading"""
        subprocess.Popen(['xdg-open', self.model.magnet])

    @Slot()
    def _download_subtitles(self):
        """Download subtitles"""
        subprocess.Popen(['xdg-open', self.model.subtitle])
