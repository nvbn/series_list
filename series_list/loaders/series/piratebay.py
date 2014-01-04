from BeautifulSoup import BeautifulSoup
import requests
from ...models import SeriesEntry
from ...settings import config
from ..base import return_if_timeout
from .. import library
from .base import SeriesLoader


@library.series
class PirateBayLoader(SeriesLoader):
    """Loader from pirate bay"""

    def _get_url(self, page, filters):
        """Get url for fetching"""
        if filters == '':
            return 'http://thepiratebay.se/browse/205/{}/3'.format(page)
        else:
            return u'http://thepiratebay.se/search/{}/{}/99/205'.format(
                filters, page,
            )

    def _fetch_html(self, page, filters):
        """Fetch html"""
        return requests.get(
            self._get_url(page, filters), timeout=config.series_timeout,
        ).content

    def _parse_html(self, html):
        """Parse received html"""
        soup = BeautifulSoup(html)
        table = soup.find('table', {'id': 'searchResult'})
        if table:
            for row in table.findAll('tr', {
                'class': lambda cls: cls != 'header',
            }):
                detail = row.find('a', {'class': 'detLink'})
                if detail:
                    yield SeriesEntry.get_or_create(
                        title=detail.text,
                        magnet=row.findAll('td')[1].findAll('a')[1]['href'],
                    )

    @return_if_timeout([])
    def get_series(self, page=0, filters=''):
        """Get series"""
        data = self._fetch_html(page, filters)
        return list(self._parse_html(data))
