class BaseModel(object):
    """Base model"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def as_dict(self):
        """Model as dict"""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }
