from urllib import urlencode
from BeautifulSoup import BeautifulSoup
import requests


class Addic7edLoader(object):
    """Subtitle loader from addicted"""

    def _get_url(self, name):
        """Get url for name"""
        return 'http://www.addic7ed.com/search.php?{}'.format(
            urlencode({'search': name, 'Submit': 'Search'}),
        )

    def _fetch_search(self, name):
        """Fetch search result"""
        return requests.get(self._get_url(name)).content

    def _get_episode_url(self, html):
        """Get episode url from html"""
        soup = BeautifulSoup(html)
        relative = soup.find('table', {'class': 'tabel'}).find('tr')\
            .findAll('td')[1].find('a')['href']
        return 'http://www.addic7ed.com/{}'.format(relative)

    def _fetch_episode(self, url):
        """Fetch episode"""
        return requests.get(url).content

    def _parse_episode(self, html):
        """Parse episode page"""
        soup = BeautifulSoup(html)
        relative = soup.find('a', {'class': 'buttonDownload'})['href']
        return 'http://www.addic7ed.com{}'.format(relative)

    def get_subtitle_url(self, name):
        """Get subtitle url"""
        # avoid recursive import
        from ..models import Subtitle

        search = self._fetch_search(name)
        try:
            episode_url = self._get_episode_url(search)
        except AttributeError:
            return None
        episode = self._fetch_episode(episode_url)
        return Subtitle(
            url=self._parse_episode(episode),
            refer=episode_url,
        )
