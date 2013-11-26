import requests


class DownloadSubtitle(object):
    """Download subtitle"""

    def download(self, subtitle):
        with open(subtitle.path, 'w') as file_o:
            file_o.write(requests.get(
                subtitle.url, headers={'Referer': subtitle.refer},
            ).content)
