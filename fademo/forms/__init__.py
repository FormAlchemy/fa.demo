# -*- coding: utf-8 -*-
from pylons import config, url
from fademo.model import admin as model
from fademo.lib.base import render
from formalchemy import config as fa_config
from formalchemy import templates
from formalchemy import validators
from formalchemy import fields
from formalchemy import forms
from formalchemy import tables
from formalchemy.ext.fsblob import FileFieldRenderer
from formalchemy.ext.fsblob import ImageFieldRenderer
import fa.jquery as jq

fa_config.encoding = 'utf-8'
fa_config.engine = jq.TemplateEngine()

## Use jquery renderers
forms.FieldSet.default_renderers.update(jq.default_renderers)
#forms.FieldSet.default_renderers['dropdown'] = jq.relations()

class FieldSet(forms.FieldSet):
    pass

class Grid(tables.Grid):
    pass

## Initialize fieldsets

User = FieldSet(model.User)
User.configure(
        exclude=[User.password_check],
        options=[User.created.readonly()])
User = jq.Tabs('user',
            ('infos', 'Infos', User),
            ('groups', 'Groups', User.copy('groups')),
            )
del User.infos.groups


Group = FieldSet(model.Group)
Group.configure(options=[
    Group.created.readonly(),
  ])
Group.configure(options=[Group.created.readonly()])
Group = jq.Tabs('groups',
            ('infos', 'Infos', Group),
            ('users', 'Users', Group.copy(Group.users)),
            ('permissions', 'permissions', Group.copy(Group.permissions)),
        )
del Group.infos.users
del Group.infos.permissions

Permission = FieldSet(model.Permission)
Permission.configure()
Permission = jq.Tabs('permissions',
            ('infos', 'Infos', Permission),
            ('groups', 'Groups', Permission.copy(Permission.groups)),
        )
del Permission.infos.groups

Widgets = FieldSet(model.Widgets)
Widgets.configure()
Widgets.autocomplete.set(renderer=jq.autocomplete(['%sanux' % s for s in 'BCDFGHJKLMNP']))

## Initialize grids

UserGrid = Grid(model.User)
UserGrid.configure(include=[
    UserGrid.username,
    UserGrid.email,
    UserGrid.groups,
    UserGrid.active,
])

