import logging
from fa.jquery.pylons import ModelsController
from webhelpers.paginate import Page
from fademo.lib.base import BaseController, render
from fademo import model
from fademo import forms
from fademo.model import meta
from fademo.lib.decorators import authorize
from fademo.lib.auth.permissions import SignedIn

log = logging.getLogger(__name__)

from pylons import request, response, url, session, tmpl_context as c
from pylons.controllers.util import abort

import simplejson as json
import datetime
import decimal

def default(self, o):
	if isinstance(o, datetime.datetime):
		return o.strftime('%Y-%m-%d %H:%M:%S')
	elif isinstance(o, datetime.date):
		return o.strftime('%Y-%m-%d')
	elif isinstance(o, decimal.Decimal):
		return str(o)
	raise TypeError("%r is not JSON serializable" % o)

json.JSONEncoder.default = default

# Has to be overriden due to JSON encoder datetime bug :(
def render_json_format(self, fs=None, **kwargs):
	from formalchemy.fields import _pk
	from formalchemy.ext.pylons.controller import model_url
	response.content_type = 'text/javascript'
	if fs:
		try:
			fields = fs.jsonify()
		except AttributeError:
			fields = dict([(field.key, field.model_value) for field in fs.render_fields.values()])
		data = dict(fields=fields)
		pk = _pk(fs.model)
		if pk:
			data['url'] = model_url(self.member_name, id=pk)
	else:
		data = {}
	data.update(kwargs)
	return json.dumps(data)

def get_jqgrid_column_model(self):
	"""
	Return grid column model as JSON for internal use of jqGrid jQuery plugin
	"""
	#import pdb; pdb.set_trace()
	columns = []
	for f in self.render_fields.itervalues():
		#import pdb; pdb.set_trace()
		# fetch labels, lookup choices and other stuff
		c = dict(name=f.name, index=f.name, label=f.label_text)
		t = f.type.__class__.__name__
		# analyse field type
		if t == 'Date' or t == 'DateTime':
			c['formatter'] = 'date'
			c['sorttype'] = 'date'
			c['align'] = 'center'
		elif t == 'Boolean':
			c['editoptions'] = dict(value={0: 'False', 1: 'True'})
			c['formatter'] = 'checkbox'
			c['stype'] = 'select'
			c['align'] = 'center'
		elif t == 'Integer':
			if not f.is_relation:
				c['align'] = 'right'
			c['formatter'] = 'number'
			c['formatoptions'] = dict(decimalPlaces=0)
			c['sorttype'] = 'int'
		elif t == 'Float':
			c['align'] = 'right'
			c['formatter'] = 'currency'
			c['sorttype'] = 'float'
		elif t == 'UnicodeText':
			c['formatter'] = 'text'
		# if the field is a relation -> grab from the related table possible values for combobox grid column
		if f.is_relation:
			# disable searching if relation is fixed via GET parameter. This is useful to show Many-end grid of the relation
			if request.GET.has_key(f.name):
				c['search'] = False
				c['defval'] = request.GET.get(f.name)
			#import pdb; pdb.set_trace()
			# TODO: this can be really lengthy -- shouldn't we use autocomplete?
			# TODO: order_by from table definition!
			order_by = f.relation_type().mapper.order_by
			#import pdb; pdb.set_trace()
			choices = dict((r.id, unicode(r)) for r in f.relation_type().query.order_by(order_by).all())
			c['formatter'] = 'select'
			c['editoptions'] = dict(value=choices)
			c['stype'] = 'select'
		# respect search options come via GET
		if request.GET.has_key(f.name):
			c['searchoptions'] = dict(defaultValue=request.GET.get(f.name))
		columns.append(c)
	return json.dumps(columns)

def index(self, format='html', **kwargs):
	"""REST api"""
	page = self.get_page()
	if format == 'json':
		values = [x.to_dict() for x in page.items]
		return self.render_json_format(records=values, page_count=page.page_count, page=page.page, record_count=page.item_count)
	fs = self.get_grid()
	fs = fs.bind(instances=page)
	fs.readonly = True
	fs.pager = page
	return self.render_grid(format=format, fs=fs, id=None, pager=page.pager(**self.pager_args))

def get_page(self):
	query = self.get_filtered_ordered_queryset()
	kwargs = request.environ.get('pylons.routes_dict', {})
	try:
		page = request.GET.get('page', '1')
	except:
		pass
	#try:
	#	kwargs['items_per_page'] = int(request.GET.get('limit'))
	#except:
	#	pass
	kwargs['page'] = page
	#return Page(query, items_per_page=20000, **kwargs)
	return Page(query, **kwargs)

# return a chunk of filtered and ordered by params dict records of specified model
def get_filtered_ordered_queryset(self):
	# cache some stuff
	model = self.get_model()
	params = request.params
	session = self.model.Session
	# get model entity fields
	fields = model._descriptor._columns
	# fetch data. TODO: include only display_fields?
	result = session.query(model)
	#import pdb; pdb.set_trace()
	# apply filters (if any)
	# TODO: make GET filter/sort parameters configurable?
	if True:
		import sqlalchemy
		for f in fields:
			#import pdb; pdb.set_trace()
			key = str(f.name)
			# skip filter unless the value provided
			if not params.has_key(key):
				continue
			value = params[key] #.decode()
			if value == '': continue
			# comparisons are: <, <=, <>, >=, >
			# N.B: multiconditions allowed, consider: <123>100 for 100 < x < 123
			import re
			for s in re.findall(r'((?:<>|=|<=?|>=?|)[^\s<>=]+)+?', value.strip()):
				s = s.strip() # value to compare to
				c = None # comparison criterion
				if len(s) > 2 and s[0:2] == '<>':
					c = 'ne'; s = s[2:]
				elif len(s) > 0:
					if s[0] == '<':
						c = 'l'; s = s[1:]
					elif s[0] == '>':
						c = 'g'; s = s[1:]
					if s[0] == '=':
						if not c is None:
							c += 'e'; s = s[1:]
						else:
							c = 'eq'; s = s[1:]
					elif not c is None:
						c += 't'
					else:
						if len(f.foreign_keys) > 0 or f.primary_key:
							c = 'eq'
						else:
							c = 'ilike'; s = '%' + s + '%'
				else:
					continue
				#print "[%s][%s]" % (c, s, )
				if not c is None and len(s) > 0:
					#import pdb; pdb.set_trace()
					if c != 'ilike': c = '__' + c + '__'
					result = result.filter(getattr(sqlalchemy.cast(f, sqlalchemy.types.String), c)(s))
	# sort result: &sortname=FIELD[&sortorder=(asc|desc)]
	# N.B. if none ordering provided -> use intrinsic model ordering from Entity's using_options(order_by='name')
	sortname = params.get('sortname', getattr(model._descriptor, 'order_by') or 'id').decode()
	#import pdb; pdb.set_trace()
	if sortname and hasattr(fields, sortname):
		sortname = getattr(fields, sortname)
		sortorder = params.get('sortorder', 'asc').decode().lower()
		if sortorder in ['asc', 'desc']:
			# N.B. workaround: order_by foreign keys should order by foreign table repr() (say, 'name' column)
			if len(sortname.foreign_keys) > 0:
				# extract the name of ManyToOne column
				#import pdb; pdb.set_trace()
				sortname = sortname.name.replace('_id', '')
				# hardcode related table column used for sorting
				colname = 'name'
				# preload related table column
				#result = result.enable_eagerloads(True)?
				#add_column(<related column here>)?
				from sqlalchemy.orm import eagerload
				result = result.options(eagerload(sortname, innerjoin=True))
				#import pdb; pdb.set_trace()
				# sort by joined field
				result = result.order_by(sortname + '_1.' + colname + ' ' + sortorder) #TODO: SQL injection here?
			else:
				result = result.order_by(getattr(sortname, sortorder)())
	return result

# monkey patch base class. Rationale: if we override these methods in AdminControllerBase,
# vanilla fs.render() would still use base class...
from formalchemy.ext.pylons.controller import _RESTController
_RESTController.render_json_format = render_json_format
_RESTController.index = index
_RESTController.get_page = get_page
_RESTController.get_filtered_ordered_queryset = get_filtered_ordered_queryset
from formalchemy.base import EditableRenderer
EditableRenderer.get_jqgrid_column_model = get_jqgrid_column_model

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

	def sync(self, fs, id=None):
		S = self.Session()
		S.add(fs.model)
		S.commit()

	def confirm(self, id=None, format='html', **kwargs):
		"""
		GET models/ID/confirm to display confirmation dialog before record deletion
		N.B. this is not standard URL for Mapper.resource(), so don't forget to make it look similar to as follows:
			map.resource('model', 'models', path_prefix='/admin/{model_name}', controller='admin', member={'confirm':'GET'})
		"""
		fs = self.get_fieldset(id=id)
		fs.readonly = True
		return self.render(format=format, fs=fs, action='confirm', id=id)

	def update_grid(self, grid):
		return

	def lookup(self):
		"""
		GET models/lookup?mask=STRING to quickly fetch JSON object of the records whose __inicode__() contains STRING, if any
		Useful for autocomplete
		N.B. this is not standard URL for Mapper.resource(), so don't forget to make it look similar to as follows:
			map.resource('model', 'models', path_prefix='/admin/{model_name}', controller='admin', collection={'lookup':'GET'})
		"""
		query = self.get_filtered_ordered_queryset()
		mask = request.GET.get('mask').lower()
		data = dict(filter(lambda x:mask in x[1].lower(), [(y.id, unicode(y)) for y in query]))
		response.content_type = 'text/javascript'
		return json.dumps(data)

AdminController = ModelsController(AdminControllerBase,
                                   prefix_name='admin',
                                   member_name='model',
                                   collection_name='models',
                                  )

