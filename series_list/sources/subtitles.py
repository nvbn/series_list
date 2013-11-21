import abc
from pony.orm import commit
from pony.utils import count
from ..models import Subtitle


class BaseSubtitleSource(object):
    """Base subtitle source"""
    __metaclass__ = abc.ABCMeta

    def _already_exists(self, subtitle):
        """Is subtitle already exists"""
        return count(Subtitle.select(lambda sub: sub.url == subtitle['url']))

    def fetch(self, episode):
        """Fetch subtitles for episode"""
        subtitles = []
        for subtitle in self._get_subtitles(episode):
            if not self._already_exists(subtitle):
                subtitles.append(Subtitle(
                    episode=episode,
                    url=subtitle['url'],
                    name=subtitle['name'],
                    language=subtitle['language'],
                ))
                commit()
        return subtitles

    @abc.abstractmethod
    def _get_subtitles(self, episode):
        """Get subtitles method"""

