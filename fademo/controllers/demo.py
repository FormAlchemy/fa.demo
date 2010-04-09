# -*- coding: utf-8 -*-
import logging

from pylons import request, tmpl_context as c

from fademo.lib.base import BaseController, render

log = logging.getLogger(__name__)

from fademo.model import *
from fademo.lib import auth
from fademo.lib.decorators import authorize
from fademo.lib.auth.permissions import SignedIn

class DemoController(BaseController):

    # Need to protect an entire controller?
    # Decorating __before__ protects all actions
    
    # @authorize(SignedIn())
    def __before__(self):
        pass
    

    def index(self):
        c.users = Session.query(User).all()
        c.groups = Session.query(Group).all()
        c.permissions = Session.query(Permission).all()
        c.title = 'Public'
        return render('test.mako')
    

    # Need to protect just a single action?
    # Do it like this ....
    @authorize(SignedIn())
    def privindex(self):
        c.users = Session.query(User).all()
        c.groups = Session.query(Group).all()
        c.permissions = Session.query(Permission).all()
        # Use this for obviousness
        # c.user = auth.get_user()
        # or this for directness
        c.user = request.environ['AUTH_USER']
        c.title = 'Private'
        return render('test.mako')
    
