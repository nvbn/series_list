from BeautifulSoup import BeautifulSoup
import requests
from ...models import SeriesEntry
from ...settings import config
from ..base import return_if_timeout
from .. import library
from .base import SeriesLoader


@library.series
class EZTVLoader(SeriesLoader):
    """eztv.it loader"""
    can_change_page_with_filter = False

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
            return requests.get(url, timeout=config.series_timeout).content
        else:
            return requests.post(url, {
                'SearchString1': filters,
                'Page': page,
            }, timeout=config.series_timeout).content

    def _parse_html(self, html):
        """Parse received html"""
        soup = BeautifulSoup(html)
        for part in soup.findAll('tr', {'class': 'forum_header_border'}):
            yield SeriesEntry.get_or_create(
                title=part.findAll('td')[1].find('a').text,
                magnet=part.findAll('td')[2].find('a')['href'],
            )

    @return_if_timeout([])
    def get_series(self, page=0, filters=''):
        """Get series"""
        data = self._fetch_html(page, filters)
        return list(self._parse_html(data))
