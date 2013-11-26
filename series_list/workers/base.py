from PySide.QtCore import QThread


class BaseWorkerThread(QThread):
    """Poster worker"""
    worker = None

    def __init__(self):
        super(BaseWorkerThread, self).__init__()
        self.receiver = self.worker()
        self.receiver.moveToThread(self)

    def __getattr__(self, name):
        """Proxy to receiver"""
        return getattr(self.receiver, name)
