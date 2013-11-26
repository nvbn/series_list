from PySide.QtGui import QWidget
from ..interface.loader import WithUiMixin


class DownloadsWidget(WithUiMixin, QWidget):
    """Downloads widget"""
    ui = 'downloads'

    def __init__(self, *args, **kwargs):
        super(DownloadsWidget, self).__init__(*args, **kwargs)
        self._update_visibility()

    @property
    def downloads_layout(self):
        """Downloads layout"""
        return self.downloadsContainer.layout()

    def _update_visibility(self):
        """Update visibility"""
        if self.downloads_layout.count():
            self.show()
        else:
            self.hide()
