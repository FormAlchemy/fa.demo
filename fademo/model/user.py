from datetime import datetime
from elixir import *
from elixir import events
import hashlib
from fademo.model import Session, metadata

options_defaults['inheritance'] = 'multi'

def encrypt_value(value):
    return hashlib.sha1(value).hexdigest()

class NotAuthenticated(Exception):pass

class User(Entity):
    username = Field(Unicode(30), required=True, unique=True) # undocumented
    password = Field(String(40), required=True, unique=True) # undocumented
    password_check = Field(String(40)) # undocumented
    email = Field(String(255), required=True) # undocumented
    created = Field(DateTime) # undocumented
    active = Field(Boolean) # undocumented
    groups = ManyToMany('Group')
    using_options(shortnames=True)

    # def __repr__(self):
    #     return '<%r %r, email: %r, created: %s, active: %s>' \
    #            % (self.__class__.__name__.capitalize(), self.username,
    #               self.email, self.created.ctime(), self.active)

    def __repr__(self):
        return self.username

    __unicode__ = __repr__

    @classmethod
    def authenticate(cls, username, password):
        try:
            user=cls.query.filter_by(username=username, active=True).one()
            if user and encrypt_value(password) == user.password:
                return user
        except Exception:
            raise NotAuthenticated
        raise NotAuthenticated

    def validate_password(user, password):
        return encrypt_value(password) == user.password

    @events.before_insert
    @events.before_update
    def encrypt_password(self):
        if self.password and self.password != self.password_check:
            self.password = encrypt_value(self.password)
            self.password_check = self.password

    @property
    def permissions(self):
        permissions = set()
        for g in self.groups:
            permissions = permissions | set(g.permissions)
        return permissions

    @property
    def permission_names(self):
        return [p.name for p in self.permissions]

    def has_permission(self, perm):
        return (perm in self.permission_names)



class Group(Entity):
    name = Field(Unicode(30), required=True, unique=True) # undocumented
    description = Field(Unicode(255)) # undocumented
    created = Field(DateTime) # undocumented
    active = Field(Boolean) # undocumented
    users = ManyToMany('User')
    permissions = ManyToMany('Permission')
    using_options(shortnames=True)

    # def __repr__(self):
    #     return '<%r %r, description: %r, created: %s, active: %s>' \
    #            % (self.__class__.__name__.capitalize(), self.name,
    #               self.description, self.created.ctime(), self.active)

    def __repr__(self):
        return self.name

    __unicode__ = __repr__

class Permission(Entity):
    name = Field(Unicode(30), required=True, unique=True) # undocumented
    description = Field(Unicode(255)) # undocumented
    groups = ManyToMany('Group', onupdate = 'CASCADE',
                        ondelete = 'CASCADE', uselist = True)
    using_options(shortnames=True)

    def __repr__(self):
        return '<%r %r, description: %r>' \
               % (self.__class__.__name__.capitalize(),
                  self.name, self.description)

    def __repr__(self):
        return self.name

    __unicode__ = __repr__


__all__ = ['User', 'Permission', 'Group', 'NotAuthenticated']
