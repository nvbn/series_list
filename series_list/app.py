import sys
from PySide.QtCore import Slot
from PySide.QtGui import QApplication
from .widgets.series_window import SeriesWindow
from .widgets.series_entry import SeriesEntryWidget
from .loaders.series import EZTVLoader


class SeriesListApp(QApplication):
    """Series list application"""

    def init(self, window):
        """Init application"""
        self.window = window
        self.eztv_loader = EZTVLoader()
        self._init_events()
        self._load_episodes()

    def _init_events(self):
        """Init events"""
        self.window.series_widget.need_more.connect(self._load_episodes)

    @Slot(int, unicode)
    def _load_episodes(self, page=0, filters=None):
        """Load episodes"""
        for episode in self.eztv_loader.get_series(page):
            entry = SeriesEntryWidget(episode)
            self.window.series_widget.add_entry(entry)


def main():
    app = SeriesListApp(sys.argv)
    window = SeriesWindow()
    window.show()
    app.init(window)
    app.exec_()


if __name__ == '__main__':
    main()
