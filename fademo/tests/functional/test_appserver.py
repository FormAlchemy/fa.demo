from fademo.tests import *

class TestAppServer(TestController):
    def test_index(self):
        response = self.app.get('/')
        # Test response...
        assert '<span style="color:lime">Shabti FormAlchemy</span>' in response
