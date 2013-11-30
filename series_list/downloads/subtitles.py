from ..loaders import library


class DownloadSubtitle(object):
    """Download subtitle"""

    def download(self, subtitle):
        library.subtitles.download(subtitle)
