import subprocess
from PySide.QtGui import QPixmap, QFrame
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
        self.model.subscribe('download_state', self._update_download_status)
        self.model.subscribe('download_percent', self._update_download_percent)

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
        if self.model.download_state == const.DOWNLOAD_PAUSED:
            self.model.resume_download()
        else:
            self.model.pause_download()

    def _download(self):
        """Start downloading"""
        self.model.download()

    def _stop(self):
        """Stop downloading"""
        if self.model.download_state == const.DOWNLOAD_FINISHED:
            self.model.remove_file()
        else:
            self.model.stop_download()

    def _update_download_percent(self, percent):
        """Update download percent"""
        self.progress.setValue(percent)
        if percent >= config.preview_minimum:
            self.openButton.show()
        else:
            self.openButton.hide()

    def _update_download_status(self, state):
        """Update download status"""
        if state == const.DOWNLOAD_FINISHED:
            self.download.hide()
            self.stopButton.show()
            self.openButton.show()
            self.progress.hide()
            self.pauseButton.hide()
            self.openButton.show()
        elif state in (const.DOWNLOADING, const.DOWNLOAD_PAUSED):
            self.download.hide()
            self.stopButton.show()
            self.progress.show()
            self.pauseButton.show()
            self.pauseButton.setChecked(state == const.DOWNLOAD_PAUSED)
        else:
            self.progress.setValue(0)
            self.download.show()
            self.stopButton.hide()
            self.openButton.hide()
            self.progress.hide()
            self.pauseButton.hide()

    def _open(self):
        """Open downloaded file"""
        subprocess.Popen(['xdg-open', self.model.path])
