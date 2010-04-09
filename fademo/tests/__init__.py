"""Pylons application test package

This package assumes the Pylons environment is already loaded, such as
when this script is imported from the `nosetests --with-pylons=test.ini`
command.

This module initializes the application via ``websetup`` (`paster
setup-app`) and provides the base testing objects.
"""
from unittest import TestCase

from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from pylons import url
from routes.util import URLGenerator
from webtest import TestApp
from datetime import datetime
import hashlib
import pylons.test
from elixir import *
from fademo.model import *
from fademo.model import meta
from fademo import model as model
from sqlalchemy import engine_from_config

__all__ = ['environ', 'url', 'TestController', 
           'TestModel', 'TestAuthenticatedController']


# Invoke websetup with the current config file
# SetupCommand('setup-app').run([pylons.test.pylonsapp.config['__file__']])

# additional imports ...
import os
from paste.deploy import appconfig
from fademo.config.environment import load_environment

here_dir = os.path.dirname(__file__)
conf_dir = os.path.dirname(os.path.dirname(here_dir))

test_file = os.path.join(conf_dir, 'test.ini')
conf = appconfig('config:' + test_file)
config = load_environment(conf.global_conf, conf.local_conf)
environ = {}

engine = engine_from_config(config, 'sqlalchemy.')
model.init_model(engine)
metadata = elixir.metadata
Session = elixir.session = meta.Session

class Individual(Entity):
    """Table 'Individual'.

    >>> me = Individual('Groucho')

    # 'name' field is converted to lowercase
    >>> me.name
    'groucho'
    """
    name = Field(String(20), unique=True)
    favorite_color = Field(String(20))

    def __init__(self, name, favorite_color=None):
        self.name = str(name).lower()
        self.favorite_color = favorite_color

setup_all()

def setup():
    pass

def teardown():
    pass

class TestModel(TestCase):
    def setUp(self):
        pass
        # # setup_all(True)
        # metadata.drop_all(bind=engine, checkfirst=True)
        # metadata.create_all(bind=engine)
        # perm = Permission(name = u"Editors",
        #                   description = u"Can edit content.")
        # meta.Session.add(perm)
        # gadmin = Group(name = u"Administrators",
        #                description = u"Administration group",
        #                created = datetime.utcnow(),
        #                active = True)
        # meta.Session.add(gadmin)
        # meta.Session.commit()
        # g = meta.Session.query(Group).filter_by(
        #             name=u"Administrators").all()
        # assert len(g) == 1
        # assert g[0] == gadmin
        # admin = User(username = u"admin",
        #              password=hashlib.sha1("admin").hexdigest(),
        #              password_check=hashlib.sha1("admin").hexdigest(),
        #              email="admin@example.com",
        #              created = datetime.utcnow(),
        #              active = True)
        # gadmin.users.append(admin)
        # gadmin.permissions.append(perm)
        # meta.Session.add(admin)
        # u = meta.Session.query(User).filter_by(
        #                     username=u"admin").all()
        # assert len(u) == 1
        # assert u[0] == admin
        # user = User(username = u"test",
        #             password=hashlib.sha1("admin").hexdigest(),
        #             password_check=hashlib.sha1("admin").hexdigest(),
        #             email="test@example.com",
        #             created = datetime.utcnow(),
        #             active = True)
        # assert user.username == u'test'
        # meta.Session.add(user)
        # groupa = Group(name = u'Subscription Members')
        # meta.Session.add(groupa)
        # assert groupa.name == u'Subscription Members'
        # perm2 = Permission(name = u'add_users')
        # meta.Session.add(perm2)
        # groupa.permissions.append(perm2)
        # meta.Session.commit()
        # assert len(groupa.permissions) == 1
        # u = meta.Session.query(User).all()
        # assert len(u) == 2
        # meta.Session.commit()
    
    def tearDown(self):
        # drop_all(engine)
        pass

class TestController(TestModel):

    def __init__(self, *args, **kwargs):
        wsgiapp = pylons.test.pylonsapp
        config = wsgiapp.config
        self.app = TestApp(wsgiapp)
        url._push_object(URLGenerator(config['routes.map'], environ))
        TestCase.__init__(self, *args, **kwargs)

class TestAuthenticatedController(TestModel):
    
    def __init__(self, *args, **kwargs):
        wsgiapp = pylons.test.pylonsapp
        config = wsgiapp.config
        self.app = TestApp(wsgiapp, extra_environ=dict(REMOTE_USER='admin'))
        url._push_object(URLGenerator(config['routes.map'], environ))
        TestCase.__init__(self, *args, **kwargs)
    
