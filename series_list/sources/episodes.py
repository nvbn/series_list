import abc
from pony.orm import commit
from pony.utils import count
from ..models import Episode, Series


class BaseEpisodeSource(object):
    """Base episode source"""
    __metaclass__ = abc.ABCMeta

    def _episode_exists(self, subtitle):
        """Is subtitle already exists"""
        return count(Episode.select(lambda sub: sub.url == subtitle['url']))
