import logging
from fa.jquery.pylons import ModelsController
from webhelpers.paginate import Page
from fademo.lib.base import BaseController, render
from fademo.model import admin as model
from fademo import forms
from fademo.model import meta
from fademo.lib.decorators import authorize
from fademo.lib.auth.permissions import SignedIn

log = logging.getLogger(__name__)

from pylons import request, response, url, session, tmpl_context as c
from pylons.controllers.util import abort

class AdminControllerBase(BaseController):
	model = model # where your SQLAlchemy mappers are
	forms = forms # module containing FormAlchemy fieldsets definitions
	# # Uncomment this to impose an authentication requirement
	# @authorize(SignedIn())
	# def __before__(self):
	#     pass
	def Session(self): # Session factory
		return meta.Session

	## customize the query for a model listing
	# def get_page(self):
	#     if self.model_name == 'Foo':
	#         return Page(meta.Session.query(model.Foo).order_by(model.Foo.bar)
	#     return super(AdminControllerBase, self).get_page()

AdminController = ModelsController(AdminControllerBase,
                                   prefix_name='admin',
                                   member_name='model',
                                   collection_name='models',
                                  )

