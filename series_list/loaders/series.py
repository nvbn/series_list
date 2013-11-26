from BeautifulSoup import BeautifulSoup
import requests
from ..models import SeriesEntry


class EZTVLoader(object):
    """eztv.it loader"""

    def _get_url(self, page):
        """Get url for fetch"""
        return 'http://eztv.it/page_{}'.format(page)

    def _fetch_html(self, page):
        """Fetch html"""
        return requests.get(self._get_url(page)).read()

    def _parse_html(self, html):
        """Parse received html"""
        soup = BeautifulSoup(html)
        for part in soup.findAll('tr', {'class': 'forum_header_border'}):
            yield SeriesEntry(
                title=part.findAll('td')[1].find('a').text,
                magnet=part.findAll('td')[2].find('a')['href'],
            )

    def get_series(self, page=0):
        """Get series"""
        data = self._fetch_html(page)
        return list(self._parse_html(data))
