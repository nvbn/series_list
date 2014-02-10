from BeautifulSoup import BeautifulSoup
import requests
from ..base import return_if_timeout
from ..exceptions import LoaderFault
from .. import library
from .base import SeriesLoader


@library.series
class EZTVLoader(SeriesLoader):
    """eztv.it loader"""
    can_change_page_with_filter = False
    hosts = [
        'https://eztv-proxy.net/',
        'http://eztv.it/',
        'http://185.19.104.70/',
    ]

    def _get_url(self, page, filters):
        """Get url for fetch"""
        if filters == '':
            return '{}page_{}'.format(self.host, page)
        else:
            return '{}search/'.format(self.host)

    def _fetch_html(self, page, filters):
        """Fetch html"""
        url = self._get_url(page, filters)
        if filters == '':
            return requests.get(url, **self.request_params).content
        else:
            return requests.post(url, {
                'SearchString1': filters,
                'Page': page,
            }, **self.request_params).content

    def _check_faults(self, html):
        """Check if eztv not work"""
        if html.find('<b style="color: #DD0000;">OFFLINE</b>') != -1:
            raise LoaderFault(self)

    def _parse_html(self, html):
        """Parse received html"""
        soup = BeautifulSoup(html)
        for part in soup.findAll('tr', {'class': 'forum_header_border'}):
            yield dict(
                title=part.findAll('td')[1].find('a').text,
                magnet=part.findAll('td')[2].find('a')['href'],
            )

    @property
    def request_params(self):
        """Add verify=false to request params"""
        params = {'verify': False}
        params.update(super(EZTVLoader, self).request_params)
        return params

    @return_if_timeout([])
    def get_series(self, page=0, filters=''):
        """Get series"""
        data = self._fetch_html(page, filters)
        self._check_faults(data)
        return list(self._parse_html(data))
