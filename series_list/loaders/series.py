from BeautifulSoup import BeautifulSoup
import requests
from ..models import SeriesEntry


class EZTVLoader(object):
    """eztv.it loader"""

    def _get_url(self, page, filters):
        """Get url for fetch"""
        if filters == '':
            return 'http://eztv.it/page_{}'.format(page)
        else:
            return 'http://eztv.it/search/'

    def _fetch_html(self, page, filters):
        """Fetch html"""
        url = self._get_url(page, filters)
        if filters == '':
            return requests.get(url).content
        else:
            return requests.post(url, {
                'SearchString1': filters,
                'Page': page,
            }).content

    def _parse_html(self, html):
        """Parse received html"""
        soup = BeautifulSoup(html)
        for part in soup.findAll('tr', {'class': 'forum_header_border'}):
            yield SeriesEntry.get_or_create(
                title=part.findAll('td')[1].find('a').text,
                magnet=part.findAll('td')[2].find('a')['href'],
            )

    def get_series(self, page=0, filters=''):
        """Get series"""
        data = self._fetch_html(page, filters)
        return list(self._parse_html(data))
