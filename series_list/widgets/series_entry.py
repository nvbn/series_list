import subprocess
import os
from PySide.QtCore import Slot
from PySide.QtGui import QWidget, QPixmap, QApplication
from ..interface.loader import WithUiMixin
from ..models import SeriesEntry


class SeriesEntryWidget(WithUiMixin, QWidget):
    """Series entry widget"""
    ui = 'series_entry'
    cache = {}

    @classmethod
    def get_or_create(cls, model, *args, **kwargs):
        """Get or create series entry widget"""
        if not model in cls.cache:
            cls.cache[model] = cls(model, *args, **kwargs)
        cls.cache[model].show()
        return cls.cache[model]

    def __init__(self, model, *args, **kwargs):
        super(SeriesEntryWidget, self).__init__(*args, **kwargs)
        self._set_model(model)
        self._init_events()

    def _set_model(self, model):
        """Ste data from model to entry"""
        self.model = model
        self._downloading = False
        self.title.setText(model.title)
        self._set_poster_pixmap()
        self._update_subtitle()
        self._update_download_status()
        QApplication.instance()\
            .poster_received.connect(self._maybe_poster_updated)
        QApplication.instance()\
            .subtitle_received.connect(self._maybe_subtitle_updated)
        QApplication.instance()\
            .downloaded.connect(self._maybe_downloaded)
        QApplication.instance()\
            .download_progress.connect(self._maybe_progress)

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

    @Slot(SeriesEntry)
    def _maybe_downloaded(self, entry):
        """Maybe downloaded updated"""
        if entry == self.model:
            self._update_download_status()

    @Slot(SeriesEntry, float)
    def _maybe_progress(self, entry, value):
        """Maybe download progress"""
        if entry == self.model:
            self.progress.setValue(value)

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
            self.download.setEnabled(True)
        else:
            self.download.setEnabled(False)

    def _init_events(self):
        """Init events and connect signals"""
        self.download.clicked.connect(self._download)
        self.stopButton.clicked.connect(self._stop)
        self.openButton.clicked.connect(self._open)

    @Slot()
    def _download(self):
        """Start downloading"""
        self._downloading = True
        self.model.stop_download = False
        QApplication.instance().need_download(self.model)
        self._update_download_status()

    @Slot()
    def _stop(self):
        """Stop downloading"""
        if self._downloading:
            self.model.stop_download = True
            self._downloading = False
            self.progress.setValue(0)
        else:
            self.model.remove_file()
            self._update_download_status()

    @Slot()
    def _update_download_status(self):
        """Update download status"""
        if os.path.exists(self.model.path):
            self.download.hide()
            self.stopButton.show()
            self.openButton.show()
            self.progress.hide()
        elif self._downloading:
            self.download.hide()
            self.stopButton.show()
            self.openButton.hide()
            self.progress.show()
        else:
            self.download.show()
            self.stopButton.hide()
            self.openButton.hide()
            self.progress.hide()

    @Slot()
    def _open(self):
        """Open downloaded file"""
        subprocess.Popen(['xdg-open', self.model.path])
