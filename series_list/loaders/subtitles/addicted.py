from urllib import urlencode
from BeautifulSoup import BeautifulSoup
import requests
from ...settings import config
from ..base import return_if_timeout
from .. import library


@library.subtitles
class Addic7edLoader(object):
    """Subtitle loader from addicted"""

    def _get_url(self, name):
        """Get url for name"""
        return u'http://www.addic7ed.com/search.php?{}'.format(
            urlencode({'search': name, 'Submit': 'Search'}),
        )

    def _fetch_search(self, name):
        """Fetch search result"""
        return requests.get(
            self._get_url(name), timeout=config.subtitle_timeout,
        ).content

    def _get_episode_url(self, html):
        """Get episode url from html"""
        soup = BeautifulSoup(html)
        relative = soup.find('table', {'class': 'tabel'}).find('tr')\
            .findAll('td')[1].find('a')['href']
        return u'http://www.addic7ed.com/{}'.format(relative)

    def _fetch_episode(self, url):
        """Fetch episode"""
        return requests.get(url, timeout=config.subtitle_timeout).content

    def _parse_episode(self, html):
        """Parse episode page"""
        soup = BeautifulSoup(html)
        relative = soup.find('a', {'class': 'buttonDownload'})['href']
        return u'http://www.addic7ed.com{}'.format(relative)

    @return_if_timeout(None)
    def get_subtitle_url(self, name):
        """Get subtitle url"""
        # avoid recursive import
        from ...models import Subtitle

        search = self._fetch_search(name)
        try:
            episode_url = self._get_episode_url(search)
        except AttributeError:
            return None
        episode = self._fetch_episode(episode_url)
        return Subtitle(
            url=self._parse_episode(episode),
            refer=episode_url,
            name=name,
        )
