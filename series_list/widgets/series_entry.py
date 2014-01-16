import subprocess
from PySide.QtGui import QPixmap, QApplication, QFrame
from ..lib.ui import WithUiMixin
from ..settings import config
from .. import const


class SeriesEntryWidget(WithUiMixin, QFrame):
    """Series entry widget"""
    ui = 'series_entry'
    cache = {}
    icons = {
        'stopButton': ('process-stop', 'series-list-stop'),
        'pauseButton': ('media-playback-pause', 'series-list-pause'),
        'openButton': ('media-playback-start', 'series-list-open'),
        'download': ('application-x-bittorrent', 'series-list-download'),
    }

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
        self.setFrameStyle(QFrame.StyledPanel)

    def _set_model(self, model):
        """Ste data from model to entry"""
        self.model = model
        self._downloading = False
        self.title.setText(model.title)
        self.model.subscribe('poster', self._set_poster_pixmap)
        self.model.subscribe('subtitle', self._update_subtitle)
        self._update_download_status()
        QApplication.instance()\
            .downloaded.connect(self._maybe_downloaded)
        QApplication.instance()\
            .download_progress.connect(self._maybe_progress)

    def _maybe_downloaded(self, entry):
        """Maybe downloaded updated"""
        if entry.magnet == self.model.magnet:
            self.model = entry
            self._update_download_status()

    def _maybe_progress(self, entry, value):
        """Maybe download progress"""
        if entry.magnet == self.model.magnet:
            self.model = entry
            self.progress.setValue(value)
            self._update_preview_state()

    def _set_poster_pixmap(self, poster):
        """Get poster pixmap"""
        pixmap = QPixmap()
        pixmap.loadFromData(poster)
        self.poster.setPixmap(pixmap)

    def _update_subtitle(self, subtitle):
        """Update subtitle status"""
        if subtitle:
            self.download.setEnabled(True)
        else:
            self.download.setEnabled(False)

    def _init_events(self):
        """Init events and connect signals"""
        self.download.clicked.connect(self._download)
        self.stopButton.clicked.connect(self._stop)
        self.openButton.clicked.connect(self._open)
        self.pauseButton.clicked.connect(self._pause)

    def _pause(self):
        """Pause or resume downloading"""
        if self.pauseButton.isChecked():
            self.model.pause_state = const.NEED_PAUSE
        else:
            self.model.pause_state = const.NEED_RESUME

    def _download(self):
        """Start downloading"""
        self._downloading = True
        self.model.stop_download = False
        QApplication.instance().need_download(self.model)
        self._update_download_status()
        self.pauseButton.setChecked(False)

    def _stop(self):
        """Stop downloading"""
        if self._downloading:
            self.model.stop_download = True
            self._downloading = False
            self.progress.setValue(0)
            self._update_download_status()
        else:
            self.model.remove_file()
            self._update_download_status()

    def _update_preview_state(self):
        """Update preview state"""
        if self._downloading:
            if self.progress.value() >= config.preview_minimum:
                self.openButton.show()
            else:
                self.openButton.hide()

    def _update_download_status(self):
        """Update download status"""
        if self.model.exists and not self.model.stop_download:
            self.download.hide()
            self.stopButton.show()
            self.openButton.show()
            self.progress.hide()
            self.pauseButton.hide()
        elif self._downloading:
            self.download.hide()
            self.stopButton.show()
            self.progress.show()
            self.pauseButton.show()
            self._update_preview_state()
        else:
            self.download.show()
            self.stopButton.hide()
            self.openButton.hide()
            self.progress.hide()
            self.pauseButton.hide()

    def _open(self):
        """Open downloaded file"""
        subprocess.Popen(['xdg-open', self.model.path])
