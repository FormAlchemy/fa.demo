# -*- coding: utf-8 -*-
"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from pylons import url, request, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from fademo import model as model

from fademo.lib.auth import get_user, redirect_to_login
from fademo.lib.helpers import get_object_or_404
from fademo.lib.decorators import authorize
import fademo.lib.auth.permissions as permissions
import fademo.lib.helpers as h


class BaseController(WSGIController):
    """
    # Subclassed as a controller thusly ...
    from authprojectname.lib.base import *

    class AuthController(BaseController):
        __permission__=permissions.SignedIn()
        __excludes__=['post', 'add_user']
        def index(self):
            return render('/index.mako')
        @authorize(permissions.InGroup('Admins'))
        def post(self):
            return 'ok'
        @authorize(permissions.HasPermission('add_users'))
        def add_user(self):
            return 'ok'
    
    """
    
    __model__ = None
    __permission__ = None
    __excludes__ = []
    
    # def __call__(self, environ, start_response):
    #     """Invoke the Controller"""
    #     # WSGIController.__call__ dispatches to the Controller method
    #     # the request is routed to. This routing information is
    #     # available in environ['pylons.routes_dict']
    #     
    #     # Insert any code to be run per request here.
    #             
    #     try:
    #         return WSGIController.__call__(self, environ, start_response)
    #     finally:
    #         model.Session.remove()
    # 

    def __call__(self, environ, start_response):
        c.ref = url(**request.environ['pylons.routes_dict'])

        # Handle session storage of flash status messages, 
        # retrieve message from session and purge the store
        try:
            flash = session.get('flash')
            if flash:
                c.flash = flash
                del session['flash']
                session.save()
        except Exception:
            pass

        # Deal with user signin

        c.user = False
        c.legend = "Anon"
        c.userid = 0
        
        # Handle testing scenario ...
        # log.debug("Signin: REMOTEUSER %s AUTHUSERID %s" % \
        #         (request.environ.get('REMOTE_USER', False),
        #          session.get('AUTH_USER_ID', False)))

        if request.environ.get('REMOTE_USER', ''):
            if request.environ.get('paste.testing', False):
                c.user = model.Session.query(model.User).filter_by(
                    username=u''+request.environ['REMOTE_USER']).one()
                c.legend = c.user.username.capitalize()
                c.userid = session['AUTH_USER_ID'] = c.user.id
                
        # Normal running mode ...
        
        elif session.get('AUTH_USER_ID', False):
            c.user = model.Session.query(model.User).get(
                                            session['AUTH_USER_ID'])
            c.legend = c.user.username.capitalize()
            c.userid = session['AUTH_USER_ID']
            
        # On with the show ...
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            # Remove the database model.Session so that there is no possibility
            # of data leaking into other interactions.
            model.Session.remove()

    def __before__(self):
        self._check_action()
        self._load_model()
        self._authorize()
        self._context()
    

    def _load_model(self):
        """
        If __model__ variable is set will automatically load model instance 
        into context if "id" is in Routes. The name used in the context is 
        the same name as the model (in lowercase); otherwise you can use 
        the __name__ attribute. 
        """ 
        if self.__model__:
            routes_id = request.environ['pylons.routes_dict']['id']
            if routes_id:
                instance = get_object_or_404(self.__model__, id=routes_id)
                name = getattr(self, 
                               '__name__', 
                               self.__model__.__name__.lower())
                setattr(c, name, instance)
    

    def _context(self):
        """
        Put common context variables in here
        """
        pass
    

    def _check_action(self):
        """
        Do a check for action: otherwise NotImplemented error raised
        
        Is this is still true? The check remains a valid thing to do but 
        perhaps this is now pointless.
        """
        action = request.environ['pylons.routes_dict']['action']
        if not hasattr(self, action):
            abort(404)
        
    
    def _authorize(self):
        """
        Flexible action/permission declarations: If the __permission__
        variable is set to a an instance of a permission such as SignedIn()
        and the action is not in the __excludes__ variable list of excluded
        actions and the permission check fails, reroute the request to the
        login controller. Fails soft.
        
        Rerouting an already signed-in user to the login page could be a
        source of misunderstanding, although it could be argued that the
        purpose is to allow the user to switch to an account that has the
        requisite permissions. It might be nice for login to detect a
        signed-in userand offer a different template for logging in to
        another account as opposed to simply signing in.
        """
        # add user to context for convenience
        c.auth_user = get_user()
        if self.__permission__ and \
            request.environ['pylons.routes_dict']['action'] \
            not in self.__excludes__ and \
            not self.__permission__.check():
            redirect_to_login()
    

# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() \
                if not __name.startswith('_') or __name == '_']
