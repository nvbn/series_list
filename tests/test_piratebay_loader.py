import sure
from unittest import TestCase
from mock import MagicMock
from series_list.loaders.series.piratebay import PirateBayLoader
from .base import get_fixture


class PirateBayLoaderCase(TestCase):
    """Pirate bay loader case"""

    def setUp(self):
        self._mock_fetch()
        self.loader = PirateBayLoader()

    def _mock_fetch(self):
        """Mock fetching data"""
        self._orig_fetch = PirateBayLoader._fetch_html
        PirateBayLoader._fetch_html = MagicMock(
            return_value=get_fixture('piratebay.html'),
        )

    def tearDown(self):
        PirateBayLoader._fetch_html = self._orig_fetch

    def test_count(self):
        """Test count of fetched"""
        self.loader.get_series().should.have.length_of(30)

    def test_have_correct_title(self):
        """Test have correct title"""
        self.loader.get_series()[0]['title'].should.be\
            .equal('Sam.and.Cat.S01E19.MyPoober.HDTV.XviD-AFG')

    def test_have_correct_magnet(self):
        """Test have correct magnet"""
        self.loader.get_series()[0]['magnet'].should.be\
            .equal('magnet:?xt=urn:btih:a81d9b59dff7d2105aef3d00f15bc3221531d'
                   'b36&dn=Sam.and.Cat.S01E19.MyPoober.HDTV.XviD-AFG&tr=udp%3'
                   'A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftra'
                   'cker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.istole.it%3A'
                   '6969&tr=udp%3A%2F%2Ftracker.ccc.de%3A80&tr=udp%3A%2F%2Fope'
                   'n.demonii.com%3A1337')
