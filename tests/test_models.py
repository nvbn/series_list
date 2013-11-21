import sure
from unittest import TestCase
from pony.orm import commit, db_session
from .base import FlushModelsMixin, in_memory_db


with in_memory_db:
    from series_list.models import Series, Episode, Subtitle, Download


class SeriesCase(FlushModelsMixin, TestCase):
    """Series test case"""

    @db_session
    def test_create(self):
        """Test create series"""
        series = Series(name='test')
        commit()
        Series.get().should.be.equal(series)


class EpisodeCase(FlushModelsMixin, TestCase):
    """Episode case"""

    @db_session
    def test_create(self):
        """Test create episode"""
        series = Series(name='test')
        episode = Episode(
            series=series,
            season=1,
            number=2,
            name='test',
        )
        commit()
        Episode.get().should.be.equal(episode)


class SubtitleCase(FlushModelsMixin, TestCase):
    """Subtitle test case"""

    @db_session
    def test_create(self):
        """Test create episode"""
        series = Series(name='test')
        episode = Episode(
            series=series,
            season=1,
            number=2,
            name='test',
        )
        subtitle = Subtitle(
            episode=episode,
            url='test',
            name='test',
            language='en',
        )
        commit()
        Subtitle.get().should.be.equal(subtitle)


class DownloadCase(FlushModelsMixin, TestCase):
    """Download test case"""

    @db_session
    def test_create(self):
        """Test create episode"""
        series = Series(name='test')
        episode = Episode(
            series=series,
            season=1,
            number=2,
            name='test',
        )
        download = Download(
            episode=episode,
            url='test',
            name='test',
            language='en',
        )
        commit()
        Download.get().should.be.equal(download)
