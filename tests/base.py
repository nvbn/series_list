import os


def get_fixture(name):
    """Get fixture content"""
    path = os.path.join(os.path.dirname(__file__), 'fixtures', name)
    with open(path) as fixture:
        return fixture.read()
