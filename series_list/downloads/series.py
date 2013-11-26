import subprocess
from .. import const


class DownloadSeries(object):
    """Download series"""

    def download(self, episode):
        """Download episode"""
        proc = subprocess.Popen([
            'aria2c', episode.magnet,
            '--index-out=1={}'.format(episode.file_name),
            '--dir={}'.format(const.DOWNLOAD_PATH),
            '--seed-time=0',
        ])
        proc.wait()
