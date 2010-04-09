# -*- coding: utf-8 -*-
from pylons import config, url
from fademo import model
from fademo.lib.base import render
from formalchemy import config as fa_config
from formalchemy import templates
from formalchemy import validators
from formalchemy import fields
from formalchemy import forms
from formalchemy import tables
from formalchemy.ext.fsblob import FileFieldRenderer
from formalchemy.ext.fsblob import ImageFieldRenderer
from fa.jquery import renderers as jquery

if config.get('storage_path'):
    # set the storage_path if we can find its setting
    FileFieldRenderer.storage_path = config.get('storage_path')
    ImageFieldRenderer.storage_path = config.get('storage_path')

# Images are stored as Upload entity and served via UploadController
def get_upload_url(self, relative_path):
    return url('upload', path_info=relative_path)
ImageFieldRenderer.get_url = get_upload_url

fa_config.encoding = 'utf-8'

class TemplateEngine(templates.TemplateEngine):
    def render(self, name, **kwargs):
        return render('/forms/%s.mako' % name, extra_vars=kwargs)
fa_config.engine = TemplateEngine()

# use jquery renderers
forms.FieldSet.default_renderers.update(jquery.default_renderers)

# allow lightweight markup in textareas
if config.get('textarea_markup'):
    jquery.MarkupTextAreaFieldRenderer.markup = config.get('textarea_markup')

# uncomment to assign rich textarea renderer to all Text fields
#forms.FieldSet.default_renderers[fatypes.Text] = jquery.RichTextAreaFieldRenderer

# 1-M and M-1 relation renderer
class RelationRenderer(fields.SelectFieldRenderer):
    def render(self, options, **kwargs):
        if self.field.is_scalar_relation:
            kwargs.update(class_='filter')
        return super(RelationRenderer, self).render(options, **kwargs);
        # get custom grid, if any. Important to be compatible to ModelsController
        #import pdb; pdb.set_trace()
        entity_name = self.field.relation_type().__name__
        grid = globals()['%sGrid' % entity_name] or Grid(self.field.relation_type())
        grid.readonly = True
        return grid.bind(getattr(self.field.model, self.field.name)).render(**kwargs)
    def render_readonly(self, options=None, **kwargs):
        value = self.field.raw_value
        if value is None:
            return ''
        def _render(item):
            if item is None:
                return ''
            from webhelpers.html import tags
            return tags.link_to(unicode(item), url('model', model_name=self.field.relation_type().__name__, id=item.id), target='_blank')
        if self.field.is_scalar_relation:
            q = self.field.query(self.field.relation_type())
            v = q.get(value)
            return _render(v)
        #import pdb; pdb.set_trace()
        if isinstance(value, list):
            return u'<br />'.join([_render(item) for item in value])
        return _render(value)

# textarea field which display just few words of potentially lenghty text
class EllipsisTextAreaFieldRenderer(jquery.RichTextAreaFieldRenderer):
    def render_readonly(self, **kwargs):
        value = super(EllipsisTextAreaFieldRenderer, self).render_readonly(**kwargs)
        from webhelpers.html.tools import strip_tags
        from webhelpers import text
        value = text.truncate(strip_tags(value), 20) if value else ''
        return value

class FieldSet(forms.FieldSet):
    pass

class Grid(tables.Grid):
    pass

## Initialize fieldsets

User = FieldSet(model.User)
User.configure(options=[User.created.readonly()])

UserAdd = FieldSet(model.User)
UserAdd.configure(exclude=[UserAdd.created])

# Upload = FieldSet(model.Upload)
# Upload.configure(options=[
#     Upload.path.set(renderer=ImageFieldRenderer),
# ])

## Initialize grids

UserGrid = Grid(model.User)
UserGrid.configure(include=[
    UserGrid.username,
    UserGrid.email,
    UserGrid.active,
    UserGrid.groups.set(renderer=RelationRenderer),
])

# UploadGrid = Grid(model.Upload)
# UploadGrid.configure(options=[
#     UploadGrid.path.set(renderer=ImageFieldRenderer),
# ])
