from .lib.settings import BaseConfig, Var
from . import const


class Config(BaseConfig):
    """Configuration object"""
    download_path = Var(const.DOWNLOAD_PATH)

    series_timeout = Var(const.SERIES_TIMEOUT)
    subtitle_timeout = Var(const.SUBTITLE_TIMEOUT)
    poster_timeout = Var(const.POSTER_TIMEOUT)

    posters_loader = Var(const.POSTERS_LOADER)
    series_loader = Var(const.SERIES_LOADER)
    subtitles_loader = Var(const.SUBTITLES_LOADER)

    preview_minimum = Var(const.PREVIEW_MINIMUM)

    max_retry = Var(const.MAX_RETRY)

    upnp = Var(const.UPNP_DEFAULT)
    natpmp = Var(const.NATPMP_DEFAULT)
    lsd = Var(const.LSD_DEFAULT)
    dht = Var(const.DHT_DEFAULT)


config = Config()
