# -*- coding: utf-8 -*-
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
# Import helpers as desired, or define your own, ie:
# from webhelpers.html.tags import checkbox, password
from webhelpers import *

from fademo.lib.auth import permissions
from fademo.lib.auth import get_user

def get_object_or_404(model, **kw):
    from pylons.controllers.util import abort
    """
    Returns object, or raises a 404 Not Found is object is not in db.
    Uses elixir-specific `get_by()` convenience function (see elixir source: 
    http://elixir.ematia.de/trac/browser/elixir/trunk/elixir/entity.py#L1082)
    Example: user = get_object_or_404(model.User, id = 1)
    """
    obj = model.get_by(**kw)
    if obj is None:
        abort(404)
    return obj

# Auth helpers

def signed_in():
    return permissions.SignedIn().check()

def in_group(group_name):
    return permissions.InGroup(group_name).check()

def has_permission(perm):
    return permissions.HasPermission(perm).check()

# ModelController helpers in support of fa templates

from routes import url_for, redirect_to
from formalchemy.ext.pylons.controller import model_url
from pylons import url, request
