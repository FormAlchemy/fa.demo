# -*- coding: utf-8 -*-
import logging

from pylons import url, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from fademo.lib.base import BaseController, render

log = logging.getLogger(__name__)

from fademo.lib import auth
from fademo.model import *
from fademo import model

class LoginController(BaseController):
    "A stub example login controller, with login and logout methods"
    
    def index(self):
        # add your login form here
        return render('login.mako')
    
    
    def signin(self):
        username = request.params.get('username')
        password = request.params.get('password')
        try:
            user = model.User.authenticate(username, password)
            auth.login(user)
            if session.get('redirect'):
                redir_url = session.pop('redirect')
                session.save()
                redirect(url(**redir_url))
            else:
                redirect(url(controller='demo', action='privindex'))
        except model.NotAuthenticated:
            # if the user visiting this controller is not 
            # authenticated the user is routed to the index
            # (above) which presents a login form.
            redirect(url.current(action='index'))
    
    
    def signout(self):
        auth.logout()
        redirect(url.current(action='index'))
    

