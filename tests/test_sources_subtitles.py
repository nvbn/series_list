import sure
from unittest import TestCase
from mock import MagicMock
from pony.orm import db_session, count, commit
from .base import FlushModelsMixin, in_memory_db


with in_memory_db:
    from series_list.sources.subtitles import BaseSubtitleSource
    from series_list.models import Episode, Series, Subtitle


class DummySubtitleSource(BaseSubtitleSource):
    """Dummy subtitle source"""
    _get_subtitles = MagicMock()


class SubtitleSourceCase(FlushModelsMixin, TestCase):
    """Subtitle source"""

    def setUp(self):
        super(SubtitleSourceCase, self).setUp()
        self.source = DummySubtitleSource()

    def _create_episode(self):
        """Create episode"""
        series = Series(name='test')
        episode = Episode(
            series=series,
            season=1,
            number=12,
            name='test',
        )
        commit()
        return episode

    @db_session
    def test_fetch_subtitles(self):
        """Test fetch subtitles"""
        episode = self._create_episode()
        self.source._get_subtitles.return_value = [
            {
                'url': 'url_{}'.format(n),
                'name': 'test',
                'language': 'en',
            } for n in range(10)
        ]
        self.source.fetch(episode).should.have.length_of(10)
        count(Subtitle.select()).should.be.equal(10)

    @db_session
    def test_no_fetch_subtitles(self):
        """Test fetch subtitles"""
        episode = self._create_episode()
        self.source._get_subtitles.return_value = [
            {
                'url': 'url',
                'name': 'test',
                'language': 'en',
            } for _ in range(10)
        ]
        self.source.fetch(episode).should.have.length_of(1)
        count(Subtitle.select()).should.be.equal(1)
