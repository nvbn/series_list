import os
from PySide.QtUiTools import QUiLoader
from PySide.QtCore import QMetaObject
from PySide.QtGui import QIcon


class UiLoader(QUiLoader):
    """
    Subclass :class:`~PySide.QtUiTools.QUiLoader` to create the user interface
    in a base instance.

    Unlike :class:`~PySide.QtUiTools.QUiLoader` itself this class does not
    create a new instance of the top-level widget, but creates the user
    interface in an existing instance of the top-level class.

    This mimics the behaviour of :func:`PyQt4.uic.loadUi`.
    """

    def __init__(self, baseinstance):
        """
        Create a loader for the given ``baseinstance``.

        The user interface is created in ``baseinstance``, which must be an
        instance of the top-level class in the user interface to load, or a
        subclass thereof.

        ``parent`` is the parent object of this loader.
        """
        QUiLoader.__init__(self, baseinstance)
        self.baseinstance = baseinstance

    def createWidget(self, class_name, parent=None, name=''):
        if parent is None and self.baseinstance:
            # supposed to create the top-level widget, return the base instance
            # instead
            return self.baseinstance
        else:
            # create a new widget for child widgets
            widget = QUiLoader.createWidget(self, class_name, parent, name)
            if self.baseinstance:
                # set an attribute for the new child widget on the base
                # instance, just like PyQt4.uic.loadUi does.
                setattr(self.baseinstance, name, widget)
            return widget


def load_ui(uifile, baseinstance=None):
    """
    Dynamically load a user interface from the given ``uifile``.

    ``uifile`` is a string containing a file name of the UI file to load.

    If ``baseinstance`` is ``None``, the a new instance of the top-level widget
    will be created.  Otherwise, the user interface is created within the given
    ``baseinstance``.  In this case ``baseinstance`` must be an instance of the
    top-level widget class in the UI file to load, or a subclass thereof.  In
    other words, if you've created a ``QMainWindow`` interface in the designer,
    ``baseinstance`` must be a ``QMainWindow`` or a subclass thereof, too.  You
    cannot load a ``QMainWindow`` UI file with a plain
    :class:`~PySide.QtGui.QWidget` as ``baseinstance``.

    :method:`~PySide.QtCore.QMetaObject.connectSlotsByName()` is called on the
    created user interface, so you can implemented your slots according to its
    conventions in your widget class.

    Return ``baseinstance``, if ``baseinstance`` is not ``None``.  Otherwise
    return the newly created instance of the user interface.
    """
    loader = UiLoader(baseinstance)
    widget = loader.load(os.path.join(
        os.path.dirname(__file__), uifile,
    ))
    QMetaObject.connectSlotsByName(widget)
    return widget


class WithUiMixin(object):
    """With ui mixin"""
    ui = None
    icons = {}

    def __init__(self, *args, **kwargs):
        super(WithUiMixin, self).__init__(*args, **kwargs)
        load_ui('{}.ui'.format(self.ui), self)
        self._init_icons()

    def _get_icon(self, icons):
        """Get icon"""
        if len(icons):
            icon, other = icons[0], icons[1:]
            fallback = self._get_icon(other)
            if fallback:
                return QIcon.fromTheme(icon, fallback=fallback)
            else:
                return QIcon.fromTheme(icon)
        else:
            return None

    def _init_icons(self):
        """Init icons"""
        for element, icons in self.icons.items():
            getattr(self, element).setIcon(self._get_icon(icons))
