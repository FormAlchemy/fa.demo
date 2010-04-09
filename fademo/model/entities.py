# -*- coding: utf-8 -*-

"""The application's model objects"""

from elixir import *
from datetime import datetime

class ObjType(Entity):
    name = Field(Unicode(60), required=True)
    objs = OneToMany('Obj', order_by='name')
    def __unicode__(self):
        return u'%s' % (self.name, )
    using_options(shortnames=True, order_by='name')

class Obj(Entity):
    objtype = ManyToOne('ObjType') #, inverse='objs')
    name = Field(Unicode(60), required=True)#, column_kwargs={'label': u'Наименование'})
    date = Field(Date, required=True)
    sum = Field(Float, required=True)
    number = Field(Integer, required=True)
    bool = Field(Boolean, required=True)
    #enum = Field(Enum([u'foobar', u'baz', u'quux', None])) # f.values
    description = Field(UnicodeText)#.set(textarea=(25, 10))
    def __unicode__(self):
        return u'<Obj "%s" (%s)>' % (self.name, self.objtype.name)
    using_options(shortnames=True, order_by='name')
