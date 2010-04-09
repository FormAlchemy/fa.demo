# -*- coding: utf-8 -*-
"""Setup the fatest application"""
import logging

import pylons.test

from fademo.config.environment import load_environment

log = logging.getLogger(__name__)

from pylons import config
from elixir import *
from fademo import model as model
from fademo.model import user

def setup_app(command, conf, vars):
    """Place any commands to setup fademo here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        config = load_environment(conf.global_conf, conf.local_conf)
    import datetime
    import hashlib
    drop_all()
    model.metadata.create_all()
    gadmin = model.user.Group(
            name = "Administrators",
            description = u"Administration group",
            created = datetime.datetime.utcnow(),
            active = True)
    model.Session.add(gadmin)
    # model.Session.commit()
    # Check the status
    g = model.Session.query(
            model.user.Group).filter_by(
                name="Administrators").all()
    assert len(g) == 1
    assert g[0] == gadmin
    admin = model.user.User(
                username = u"admin", 
                password=hashlib.sha1("admin").hexdigest(),
                password_check=hashlib.sha1("admin").hexdigest(), 
                email="admin@example.com",
                created = datetime.datetime.utcnow(),
                active = True)
    model.Session.add(admin)
    gadmin.users.append(admin)
    # model.Session.add(gadmin)
    model.Session.commit()
    # Check the status
    u = model.Session.query(
            model.user.User).filter_by(
                username=u"admin").all()
    assert len(u) == 1
    assert u[0] == admin
    # load fixtures
    from fademo.lib.fixtures import lorem_ipsum_all
    lorem_ipsum_all(30)
    model.Session.commit()
