from fademo.lib.auth import get_user
from fademo import model

# Common permissions. Permission classes must have a 'check'
# method which returns True or False.

class SignedIn(object):

    def check(self):
        return (get_user() is not None)

class InGroup(object):

    def __init__(self, group_name):
        self.group_name = group_name 

    def check(self):
        group = model.Group.filter_by(name = self.group_name, active = True)
        if group and get_user() in group.members:
            return True
        return False

class HasPermission(object):

    def __init__(self, permission):
        self.permission = permission

    def check(self):
        user = get_user()
        if user and user.has_permission(self.permission):
            return True
        return False