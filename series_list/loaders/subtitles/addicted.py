from urllib import urlencode
from BeautifulSoup import BeautifulSoup
import requests
from ...models import Subtitle
from ..base import return_if_timeout
from .. import library
from .base import SubtitlesLoader


@library.subtitles
class Addic7edLoader(SubtitlesLoader):
    """Subtitle loader from addicted"""
    hosts = [
        'http://www.addic7ed.com/',
    ]

    def _get_url(self, name):
        """Get url for name"""
        return u'{}search.php?{}'.format(
            self.host,
            urlencode({'search': name.encode('utf8'), 'Submit': 'Search'}),
        )

    def _fetch_search(self, name):
        """Fetch search result"""
        return requests.get(
            self._get_url(name), timeout=self.timeout,
        ).content

    def _get_episode_url(self, html):
        """Get episode url from html"""
        soup = BeautifulSoup(html)
        relative = soup.find('table', {'class': 'tabel'}).find('tr')\
            .findAll('td')[1].find('a')['href']
        return u'http://www.addic7ed.com/{}'.format(relative)

    def _fetch_episode(self, url):
        """Fetch episode"""
        return requests.get(url, timeout=self.timeout).content

    def _parse_episode(self, html):
        """Parse episode page"""
        soup = BeautifulSoup(html)
        relative = soup.find('a', {'class': 'buttonDownload'})['href']
        return u'http://www.addic7ed.com{}'.format(relative)

    @return_if_timeout(None)
    def get_subtitle_url(self, name):
        """Get subtitle url"""
        search = self._fetch_search(name)
        try:
            episode_url = self._get_episode_url(search)
        except AttributeError:
            return None
        episode = self._fetch_episode(episode_url)
        return dict(
            url=self._parse_episode(episode),
            refer=episode_url,
            name=name,
        )

    def download(self, model):
        """Download subtitles"""
        with open(model.path, 'w') as file_o:
            file_o.write(requests.get(
                model.url, headers={'Referer': model.refer},
            ).content)
