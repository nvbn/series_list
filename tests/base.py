from pony.orm import db_session, commit
from series_list import const


class FlushModelsMixin(object):
    """Flush models mixin"""

    def setUp(self):
        """Flush models"""
        with in_memory_db:
            from series_list import models
        with db_session:
            self._delete_all(models.Episode)
            self._delete_all(models.Series)
            commit()

    def _delete_all(self, model):
        """Delete all model items"""
        for item in model.select():
            item.delete()


class InMemoryDB(object):
    """Base test case"""

    def __enter__(self):
        """Use in memory db"""
        self._orig_db_path = const.DB_PATH
        const.DB_PATH = ':memory:'

    def __exit__(self, *args, **kwargs):
        const.DB_PATH = self._orig_db_path


in_memory_db = InMemoryDB()
