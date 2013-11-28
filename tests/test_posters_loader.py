import sure
from unittest import TestCase
from mock import MagicMock
from series_list.loaders.posters.imdb import IMDBPosterLoader
from .base import get_fixture


class IMDBPosterLoaderCase(TestCase):
    """IMDb poster loader case"""

    def setUp(self):
        self.loader = IMDBPosterLoader()
        self._mock_fetch()

    def _mock_fetch(self):
        """Mock fetching data"""
        self._orig_fetch =self.loader._fetch_html
        self.loader._fetch_html = MagicMock()

    def test_get_poster(self):
        """Test get poster"""
        self.loader._fetch_html.return_value = get_fixture('imdb.html')
        self.loader.get_poster('family gut').should.be\
            .equal('http://ia.media-imdb.com/images/M/MV5BMTY4MjIwMjcxMF5BMl5'
                   'BanBnXkFtZTYwMDA1NDg5._V1_SY44_CR0,0,32,44_.jpg')

    def test_get_default_poster_if_not_exists(self):
        """Test get default poster if not exists"""
        self.loader._fetch_html.return_value =\
            get_fixture('imdb_none.html')
        self.loader.get_poster('family gut').should.be.\
            equal(self.loader.default_poster)
