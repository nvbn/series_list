import sure
from unittest import TestCase
from mock import MagicMock
from series_list.loaders import register


class TypedRegisterCase(TestCase):
    """Typed register case"""

    def setUp(self):
        self._mock_config()
        self._create_register()

    def _create_register(self):
        """Create register"""
        self.register = register.TypedRegister('test')

        @self.register
        class Cat(object):
            def meow(self):
                return 6

        register.config.test = 'Cat'
        self.cls = Cat

    def _mock_config(self):
        """Mock config"""
        self._orig_config = register.config
        register.config = MagicMock()

    def tearDown(self):
        register.config = self._orig_config

    def test_register_cls(self):
        """Test register cls"""
        'Cat'.should.be.within(self.register._items)

    def test_get_active(self):
        """Test get active"""
        type(self.register._active).should.be.equal(self.cls)

    def test_proxy_calls(self):
        """Test proxy calls to active"""
        self.register.meow().should.be.equal(6)

    def test_get_names(self):
        """Test get names"""
        self.register.names.should.be.equal(['Cat'])
