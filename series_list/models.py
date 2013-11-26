from .loaders.posters import IMDBPosterLoader


class SeriesEntry(object):
    """Series entry model"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.poster = IMDBPosterLoader().get_default_poster_data()

    def __repr__(self):
        return self.title

    def load_poster(self):
        """Get poster from loader"""
        self.poster = IMDBPosterLoader().get_poster_data(self.title)
