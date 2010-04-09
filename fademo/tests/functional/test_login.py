from pylons import url
from fademo.tests import *

class TestLoginController(TestController):
    def test_index(self):
        response = self.app.get(url(controller='login'))
        assert 'action="/login/signin"' in response
    
