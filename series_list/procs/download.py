import time
import libtorrent
from ..lib.actors import Actor
from ..loaders import library
from ..models import Subtitle
from ..settings import config
from .. import const
from .base import WithLibraryMixin


class VideoDownloadHandler(object):
    """Video download handler"""

    def __init__(self, uri, title):
        self._uri = uri
        self.file_name = title
        self.extension = ''

    def start(self):
        """Start downloading"""
        self._session = libtorrent.session()
        self._handle = libtorrent.add_magnet_uri(
            self._session, self._uri, {
                'save_path': config.download_path,
            }
        )
        self._wait_metadata()
        self._move_biggest_file()
        self._handle.set_sequential_download(True)

    def _wait_metadata(self):
        """Wait while metadata receiving"""
        while not self._handle.has_metadata():
            time.sleep(0.5)

    def _move_biggest_file(self):
        """Move biggest file"""
        biggest_index, biggest = max(enumerate(
            self._handle.get_torrent_info().files(),
        ), key=lambda item: item[1].size)
        self.extension = biggest.path.split('.')[-1]
        self.file_name = '{}.{}'.format(self.file_name, self.extension)
        self._handle.rename_file(biggest_index, self.file_name)

    @property
    def finished(self):
        """Is finished"""
        return self._handle.status().state == libtorrent.torrent_status.seeding

    @property
    def percent(self):
        """Downloading percent"""
        if self.finished:
            return 100
        percent = self._handle.status().progress * 100
        if percent == 100 and not self.finished:
            return 99
        else:
            return percent

    def stop(self):
        """Stop downloading and remove"""
        self._session.remove_torrent(self._handle)

    def __getattr__(self, item):
        """Proxy to original handle"""
        return getattr(self._handle, item)


class DownloadActor(WithLibraryMixin, Actor):
    """Actor for downloading content"""
    self_loop = True

    def run(self):
        super(DownloadActor, self).run()
        self._handlers = {}
        while True:
            self.loop_tick()
            time.sleep(0.5)

    def download_video(self, uri, title):
        """Download video file"""
        handler = VideoDownloadHandler(uri, title)
        self._handlers[uri] = handler
        handler.start()
        return handler.extension

    def download_subtitle(self, subtitle):
        """Download subtitle"""
        subtitle = Subtitle(**subtitle)
        library.subtitles.download(subtitle)
        return True

    def pause(self, uri):
        """Pause downloading"""
        return self._handlers[uri].pause()

    def resume(self, uri):
        """Resume downloading"""
        return self._handlers[uri].resume()

    def get_percent(self, uri):
        """Get downloading percent"""
        try:
            return self._handlers[uri].percent
        except KeyError:
            return const.NO_PERCENT

    def stop(self, uri):
        """Stop downloading"""
        self._handlers[uri].stop()
        del self._handlers[uri]
