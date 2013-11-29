import time
import libtorrent
from ..settings import config


class DownloadHandler(object):
    """Download handler"""

    def __init__(self, session, handle):
        self._session = session
        self._handle = handle

    @property
    def finished(self):
        """Is finished"""
        return self._handle.status().state == libtorrent.torrent_status.seeding

    @property
    def percent(self):
        """Downloading percent"""
        return self._handle.status().progress * 100

    def remove(self):
        """Remove torrent"""
        self._session.remove_torrent(self._handle)

    def __getattr__(self, item):
        """Proxy to original handle"""
        return getattr(self._handle, item)


class DownloadSeries(object):
    """Download series"""

    def download(self, episode):
        """Download episode"""
        session = libtorrent.session()
        handle = libtorrent.add_magnet_uri(
            session, episode.magnet, {
                'save_path': config.download_path,
            }
        )
        while not handle.has_metadata():
            time.sleep(0.5)
        handle.rename_file(0, episode.file_name)
        handle.set_sequential_download(True)
        return DownloadHandler(session, handle)
