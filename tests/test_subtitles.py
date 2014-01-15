import sure
from unittest import TestCase
from mock import MagicMock
from series_list.loaders.subtitles.addicted import Addic7edLoader
from .base import get_fixture


class Addic7edLoaderCase(TestCase):
    """Subtitles loader case"""

    def setUp(self):
        self._mock_fetch()
        self.loader = Addic7edLoader()

    def _mock_fetch(self):
        """Mock fetching data"""
        self._orig_fetch_search = Addic7edLoader._fetch_search
        self._orig_fetch_episode = Addic7edLoader._fetch_episode
        Addic7edLoader._fetch_search = MagicMock(
            return_value=get_fixture('addicted.html'),
        )
        Addic7edLoader._fetch_episode = MagicMock(
            return_value=get_fixture('addicted_single.html'),
        )

    def tearDown(self):
        Addic7edLoader._fetch_search = self._orig_fetch_search
        Addic7edLoader._fetch_episode = self._orig_fetch_episode

    def test_get_subtitle_url(self):
        """Test get subtitle url"""
        self.loader.get_subtitle_url('family guy')['url'].should.be\
            .equal('http://www.addic7ed.com/original/71889/0')

    def test_get_none_when_not_found(self):
        """Tet get none when not found"""
        Addic7edLoader._fetch_search = MagicMock(
            return_value=get_fixture('addicted_none.html'),
        )
        self.loader.get_subtitle_url('family guy').should.be.none
