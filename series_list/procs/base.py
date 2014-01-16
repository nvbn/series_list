from ..loaders import library


class WithLibraryMixin(object):
    """Mixin for actors with library"""

    def run(self):
        library.import_all()
        super(WithLibraryMixin, self).run()
