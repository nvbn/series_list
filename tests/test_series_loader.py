import sure
from unittest import TestCase
from mock import MagicMock
from series_list.loaders.series.eztv import EZTVLoader
from .base import get_fixture


class EZTVLoaderCase(TestCase):
    """EZTV loader case"""

    def setUp(self):
        self._mock_fetch()
        self.loader = EZTVLoader()

    def _mock_fetch(self):
        """Mock fetching data"""
        self._orig_fetch = EZTVLoader._fetch_html
        EZTVLoader._fetch_html = MagicMock(
            return_value=get_fixture('eztv.html'),
        )

    def tearDown(self):
        EZTVLoader._fetch_html = self._orig_fetch

    def test_count(self):
        """Test count of fetched"""
        self.loader.get_series().should.have.length_of(50)

    def test_have_correct_title(self):
        """Test have correct title"""
        self.loader.get_series()[0].title.should.be\
            .equal('Wildest Islands 2of8 Carribean 720p x'
                   '264 AC3 HDTV-MVGroup')

    def test_have_correct_magnet(self):
        """Test have correct magnet"""
        self.loader.get_series()[0].magnet.should.be\
            .equal('magnet:?xt=urn:btih:FE1AC8B268B008C18120403357E4C06301012'
                   '953&dn=Wildest.Islands.2of8.Carribean.720p.x264.AC3.HDTV'
                   '-MVGroup&tr=http://www.mvgroup.org:2710/announce&tr=udp:'
                   '//tracker.openbittorrent.com:80&tr=udp://tracker.publicb'
                   't.com:80&tr=udp://tracker.istole.it:80&tr=udp://open.dem'
                   'onii.com:80&tr=udp://tracker.coppersurfer.tk:80')
