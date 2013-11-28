from PySide.QtCore import Slot
from PySide.QtGui import QDialog, QFileDialog
from ..interface.loader import WithUiMixin
from ..settings import config


class SettingsDialog(WithUiMixin, QDialog):
    """Settings dialog"""
    ui = 'settings'

    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)
        self._set_initial_values()
        self._init_events()

    def accept(self, *args, **kwargs):
        super(SettingsDialog, self).accept(*args, **kwargs)
        self._save_changes()

    def _init_events(self):
        """Connect signals with slots"""
        self.changeDownloadsPath.clicked.connect(self._change_path)

    @Slot()
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

    def _set_initial_values(self):
        """Set initial values"""
        self._update_path(config.download_path)
        self.posterTimeout.setValue(self._timeout_from_settings(
            config.poster_timeout,
        ))
        self.seriesTimeout.setValue(self._timeout_from_settings(
            config.series_timeout,
        ))
        self.subtitlesTimeout.setValue(self._timeout_from_settings(
            config.subtitle_timeout,
        ))

    def _timeout_to_settings(self, value):
        """Convert timeout to settings format"""
        if value == 0:
            return None
        else:
            return value

    def _save_changes(self):
        """Save changes"""
        config.download_path = self._download_path
        config.poster_timeout = self._timeout_to_settings(
            self.posterTimeout.value(),
        )
        config.series_timeout = self._timeout_to_settings(
            self.seriesTimeout.value(),
        )
        config.subtitle_timeout = self._timeout_to_settings(
            self.subtitlesTimeout.value(),
        )
