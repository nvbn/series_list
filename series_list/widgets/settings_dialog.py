from PySide.QtGui import QDialog, QFileDialog
from ..lib.ui import WithUiMixin
from ..settings import config
from ..loaders import library


class SettingsDialog(WithUiMixin, QDialog):
    """Settings dialog"""
    ui = 'settings'

    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)
        self._timeouts = (
            (self.posterTimeout, 'poster_timeout'),
            (self.seriesTimeout, 'series_timeout'),
            (self.subtitlesTimeout, 'subtitle_timeout'),
            (self.retryCount, 'max_retry'),
        )
        self._loaders = (
            (self.postersProviders, 'posters_loader', library.posters),
            (self.seriesProviders, 'series_loader', library.series),
            (self.subtitlesProviders, 'subtitles_loader', library.subtitles),
        )
        self._set_initial_values()
        self._init_events()

    def accept(self, *args, **kwargs):
        super(SettingsDialog, self).accept(*args, **kwargs)
        self._save_changes()

    def _init_events(self):
        """Connect signals with slots"""
        self.changeDownloadsPath.clicked.connect(self._change_path)

    def _change_path(self):
        """Change downloads path"""
        self._update_path(QFileDialog.getExistingDirectory(self))

    def _update_path(self, path):
        """Update download path"""
        self._download_path = path
        self.downloadsPathLabel.setText(u'Downloads path:\n {}'.format(path))

    def _timeout_from_settings(self, value):
        """Timeout from settings"""
        if value is None:
            return 0
        else:
            return value

    def _load_timeout(self, widget, value):
        """Load timeout from value"""
        widget.setValue(self._timeout_from_settings(value))

    def _load_loader(self, widget, current, available):
        """Load loader from settings"""
        widget.addItems(available)
        widget.setCurrentIndex(available.index(current))

    def _set_initial_values(self):
        """Set initial values"""
        self._update_path(config.download_path)
        for widget, settings_name in self._timeouts:
            self._load_timeout(widget, getattr(config, settings_name))
        for widget, settings_name, register in self._loaders:
            self._load_loader(
                widget, getattr(config, settings_name), register.names,
            )
        self.previewPercent.setValue(config.preview_minimum)

    def _timeout_to_settings(self, value):
        """Convert timeout to settings format"""
        if value == 0:
            return None
        else:
            return value

    def _save_timeout(self, widget, settings_name):
        """Save timeout to settings"""
        setattr(config, settings_name, self._timeout_to_settings(
            widget.value(),
        ))

    def _save_loader(self, widget, settings_name):
        """Save loader to settings"""
        setattr(config, settings_name, self._timeout_to_settings(
            widget.currentText(),
        ))

    def _save_changes(self):
        """Save changes"""
        config.download_path = self._download_path
        for widget, settings_name in self._timeouts:
            self._save_timeout(widget, settings_name)
        for widget, settings_name, _ in self._loaders:
            self._save_loader(widget, settings_name)
        config.preview_minimum = self.previewPercent.value()
