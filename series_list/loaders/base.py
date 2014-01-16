import abc
from copy import copy
import requests
from decorator import decorator
from ..lib.lazy import lazy_for_all
from .exceptions import LoaderFault


class BaseLoader(object):
    """Base loader class"""
    __metaclass__ = abc.ABCMeta
    hosts = []

    @abc.abstractproperty
    def timeout(self):
        """Timeout for loader"""

    @lazy_for_all
    def host(self):
        """Return first reachable host"""
        for host in self.hosts:
            if self._check_host(host):
                return host
        raise LoaderFault('No working hosts')

    def _check_host(self, host):
        """Check is host available"""
        try:
            requests.head(host, timeout=self.timeout)
            return True
        except requests.ConnectionError:
            return False


def return_if_timeout(return_value_or_method, is_method=False):
    """Return value if timeout"""
    @decorator
    def return_if_timeout_decorator(fnc, *args, **kwargs):
        try:
            return fnc(*args, **kwargs)
        except requests.Timeout:
            if is_method:
                return getattr(args[0], return_value_or_method)()
            else:
                return copy(return_value_or_method)
    return return_if_timeout_decorator


def _create_words_set(name):
    """Create words set"""
    return set(''.join([
        char if char.isalpha() or char.isdigit() else ' '
        for char in name.lower()
    ]).split(' '))


def similarity(first, second):
    """Get similarity between texts"""
    first_set = _create_words_set(first)
    second_set = _create_words_set(second)
    return len(first_set.intersection(second_set)) \
        - len(first_set.difference(second_set))
