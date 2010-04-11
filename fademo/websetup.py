# -*- coding: utf-8 -*-
"""Setup the fatest application"""
import logging
import random

import pylons.test

from fademo.config.environment import load_environment

log = logging.getLogger(__name__)

from pylons import config
from elixir import *
from fademo import model as model
from fademo.model import user
from fademo.model import demo

def setup_app(command, conf, vars):
    """Place any commands to setup fademo here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        config = load_environment(conf.global_conf, conf.local_conf)
    import datetime
    import hashlib
    drop_all()
    model.metadata.create_all()
    for name in (u'Administrators', u'Moderators', u'Users'):
        g = model.user.Group(
                name = name,
                description = u"%s group" % name,
                created = datetime.datetime.utcnow(),
                active = True)
        model.Session.add(g)
    g = model.Session.query(
            model.user.Group).filter_by(
                name="Administrators").first()
    ug = model.Session.query(
            model.user.Group).filter_by(
                name="Users").first()
    for i, name in enumerate(('admin', 'bob', 'josette', 'bernard', 'gertrude', 'jacques', 'lise', 'robert', 'jacqueline')):
        user = model.user.User(
                    username = name.title(),
                    password=hashlib.sha1(name).hexdigest(),
                    password_check=hashlib.sha1(name).hexdigest(),
                    email="%s@example.com" % name,
                    created = datetime.datetime.utcnow(),
                    active = True)
        model.Session.add(user)
        ug.users.append(user)
        if i < 3:
            g.users.append(user)

    for i, name in enumerate(('read', 'write', 'admin')):
        perm = model.user.Permission(
                name = name.title(),
                description = '%s permission' % name.title(),
                )
        model.Session.add(perm)
        if i > 1:
            g.permissions.append(perm)
        else:
            ug.permissions.append(perm)

    for i in range(50):
        article = demo.Article(
                title='Article %s' % i,
                text='''Heading
=====================

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent consectetur
imperdiet porta. Pellentesque habitant morbi tristique senectus et netus et
malesuada fames ac turpis egestas. Proin sollicitudin, mi sit amet blandit
dignissim, lacus ante sagittis est, in congue lectus nulla non urna. Nunc a
justo ut lacus laoreet facilisis. Nullam blandit posuere mauris semper
pellentesque. Sed leo neque, vulputate sed pharetra vel, rhoncus at nisl.
Aenean eget nibh turpis. Quisque semper lacus sodales libero dictum pretium.
Phasellus euismod, odio sit amet vehicula pharetra, nunc diam imperdiet dui,
non malesuada neque erat ac augue. Sed elit ipsum, placerat vitae accumsan
quis, tempor in tellus. Vestibulum tempus consequat libero, sit amet
pellentesque lacus interdum in. Vestibulum in nunc at nulla ultrices laoreet.

* Morbi id orci augue, porta malesuada mi.
* Proin rhoncus tellus non orci iaculis pretium.
* Praesent aliquet commodo urna, vitae laoreet arcu porttitor ut.
* Nullam sollicitudin blandit risus, eu luctus nisl scelerisque eget.


Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent consectetur
imperdiet porta. Pellentesque habitant morbi tristique senectus et netus et
malesuada fames ac turpis egestas. Proin sollicitudin, mi sit amet blandit
dignissim, lacus ante sagittis est, in congue lectus nulla non urna. Nunc a
justo ut lacus laoreet facilisis. Nullam blandit posuere mauris semper
pellentesque. Sed leo neque, vulputate sed pharetra vel, rhoncus at nisl.
Aenean eget nibh turpis. Quisque semper lacus sodales libero dictum pretium.
Phasellus euismod, odio sit amet vehicula pharetra, nunc diam imperdiet dui,
non malesuada neque erat ac augue. Sed elit ipsum, placerat vitae accumsan
quis, tempor in tellus. Vestibulum tempus consequat libero, sit amet
pellentesque lacus interdum in. Vestibulum in nunc at nulla ultrices laoreet.
''',
            publication_date = datetime.datetime.utcnow())
        model.Session.add(article)

    for i in range(100):
        widgets = demo.Widgets(
                autocomplete=random.choice(['%sanux' % s for s in 'BCDFGHJKLMNP']+['']),
                color = random.choice(["#EEEEEE", "#FFFF88", "#FF7400", "#CDEB8B", "#6BBA70"]),
                slider = random.choice(range(0, 100, 10)),
                )
        model.Session.add(widgets)

    model.Session.commit()

