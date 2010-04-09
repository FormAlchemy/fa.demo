from fademo.tests import *
from fademo import model

class TestUser(TestModel):
    def setUp(self):
        TestModel.setUp(self)
        self.user = model.User(username = u'tester', password = 'test', 
                               email = 'test@here.com', active = True)
        self.group = model.Group(name = u'Subscription Members')
        self.group.permissions.append(model.Permission(name = u'add_users'))
        model.Session.commit()
    def test_authenticate(self):
        assert model.User.authenticate(u'tester', 'test')
        self.user.password = 'test_again'
        print(self.user)
        model.Session.commit()
        assert model.User.authenticate(u'tester', 'test_again')
    def test_permissions(self):
        assert not self.user.has_permission(u'add_users')
        self.group.users.append(self.user)        
        model.Session.commit()
        self.user.refresh()
        assert self.user.has_permission(u'add_users')
