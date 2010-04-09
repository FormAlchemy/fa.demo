from pylons import request, session, url
from pylons.controllers.util import redirect
from fademo import model as model

_login_url = 'login'
_auth_user_environ_key = 'AUTH_USER'
_auth_user_session_key = 'AUTH_USER_ID'

def get_user():
    if _auth_user_environ_key not in request.environ:
        user_id = session.get(_auth_user_session_key)
        if user_id:
            user = model.User.get_by(id = user_id, active = True)
            request.environ[_auth_user_environ_key] = user
        else:
            request.environ[_auth_user_environ_key] = None
    return request.environ[_auth_user_environ_key]

def login(user):
    session[_auth_user_session_key] = str(user.id)
    session.save()

def logout():
    session.pop(_auth_user_session_key, None)
    session.clear()
    session.delete()

def redirect_to_login():
    redirect(url(controller=_login_url))



