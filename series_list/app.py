import sys
from PySide.QtGui import QApplication
from .widgets.series_window import SeriesWindow


class SeriesListApp(QApplication):
    """Series list application"""


def main():
    app = SeriesListApp(sys.argv)
    window = SeriesWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
