import pylons
from decorator import decorator
from fademo.lib.auth import redirect_to_login

import logging
log = logging.getLogger(__name__)

def authorize(permission):
    
    """Decorator for authenticating individual actions. Takes a permission 
    instance as argument(see lib/permissions.py for examples)"""
    def wrapper(func, self, *args, **kw):
        if permission.check():
            return func(self, *args, **kw)
        pylons.session['redirect'] = \
                pylons.request.environ['pylons.routes_dict']
        pylons.session.save()
        redirect_to_login()
    return decorator(wrapper)

# Alternatively, use the decorators listed below, taken from 
# Ben Bangert's pastie:
# http://pylonshq.com/pasties/ad4b1f541220b4099c97d573a6673e41
# N.B. Assumed to be implemented:
# User.in_group(self, group): returns True or False
# User.computed_permissions(self): returns list_of_computed_permissions
#
from fademo.model import meta
from pylons.controllers.util import abort

def in_group(group):
    """Requires a user to be logged in, and the group specified"""
    def wrapper(func, *args, **kwargs):
        user = pylons.tmpl_context.user
        if not user:
            log.debug("No user logged in for permission restricted function")
            abort(401, "Not Authorized")
        if user.in_group(group):
            log.debug("User %s verified in group %s", user, group)
            return func(*args, **kwargs)
        else:
            log.debug("User %s not in group %s", user, group)
            abort(401, "Not Authorized")
    return decorator(wrapper)

def not_in_group(group):
    """Requires a user to be logged in, and NOT in the group specified"""
    def wrapper(func, *args, **kwargs):
        user = pylons.tmpl_context.user
        if not user:
            log.debug("No user logged in for permission restricted function")
            abort(401, "Not Authorized")
        if not user.in_group(group):
            log.debug("User %s verified in group %s", user, group)
            return func(*args, **kwargs)
        else:
            log.debug("User %s not in group %s", user, group)
            abort(401, "Not Authorized")
    return decorator(wrapper)
    

def has_permission(permission):
    """Requires a user to be logged in, and have the permission"""
    def wrapper(func, *args, **kwargs):
        user = pylons.tmpl_context.user
        if not user:
            log.debug("No user logged in for permission restricted function")
            abort(401, "Not Authorized")
        if permission in user.computed_permissions():
            log.debug("User %s verified in group %s", user, permission)
            return func(*args, **kwargs)
        else:
            log.debug("User %s does not have permission %s", user, permission)
            abort(401, "Not Authorized")
    return decorator(wrapper)

@decorator
def logged_in(func, *args, **kwargs):
    user = pylons.tmpl_context.user
    if not user:
        log.debug("No user logged in for permission restricted function")
        abort(401, "Not Authorized")
    return func(*args, **kwargs)