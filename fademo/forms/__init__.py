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
from fa.jquery import renderers as jq
from fa.jquery import forms as jqforms

fa_config.encoding = 'utf-8'

class TemplateEngine(templates.TemplateEngine):
    def render(self, name, **kwargs):
        return render('/forms/%s.mako' % name, extra_vars=kwargs)
fa_config.engine = TemplateEngine()

# use jquery renderers
forms.FieldSet.default_renderers.update(jq.default_renderers)

class FieldSet(forms.FieldSet):
    pass

class Grid(tables.Grid):
    pass

## Initialize fieldsets

User = FieldSet(model.User)
User.configure(
        exclude=[User.password_check],
        options=[
                 User.created.readonly(),
                 User.groups.set(renderer=jq.checkboxset()),
              ])

User = jqforms.Tabs('user',
            ('infos', 'Infos', User),
            ('groups', 'Groups', User.copy('groups')),
            )
del User.infos.groups


Group = FieldSet(model.Group)
Group.configure(options=[
    Group.created.readonly(),
    Group.users,
    Group.permissions,
  ])
Group.configure(options=[Group.created.readonly()])

Group = jqforms.Tabs('groups',
            ('infos', 'Infos', Group),
            ('users', 'Users', Group.copy(Group.users)),
            ('permissions', 'permissions', Group.copy(Group.permissions)),
        )
del Group.infos.users
del Group.infos.permissions

Permission = FieldSet(model.Permission)
Permission.configure()

Permission = jqforms.Tabs('permissions',
            ('infos', 'Infos', Permission),
            ('groups', 'Groups', Permission.copy(Permission.groups)),
        )
del Permission.infos.groups

## Initialize grids

UserGrid = Grid(model.User)
UserGrid.configure(include=[
    UserGrid.username,
    UserGrid.email,
    UserGrid.groups,
    UserGrid.active,
])


