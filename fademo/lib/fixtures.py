# -*- coding: utf-8 -*-
import types
import sys
import os
import simplejson

from fademo import model as model

"""
This module can be used for loading data into your models, for example when
setting up default application data, unit tests, JSON export/import and
importing/exporting legacy data. Data is serialized to and from the JSON
format.
"""

VALID_FIXTURE_FILE_EXTENSIONS = ['.json']

def load_data(model, filename=None, base_dir=None):
    """\
    Installs provided fixture files into given model. Filename may be a
    directory, file or list of dirs or files.
    If ``filename`` is ``None``, assumes that source file is located in
    :file:`fixtures/model_module_name/model_tablename.yaml` of the
    application directory, e.g. :file:`MyProject/fixtures/news/newsitems.yaml`.
    The base_dir argument is the top package of the application unless
    specified. You can also pass the name of a table instead of a model
    class.
    """

    if type(model) is types.StringType:
        return load_data_to_table(model, filename, base_dir)
    else:
        if filename is None:
            filename = _default_fixture_path_for_model(model, base_dir)
        return _load_data_from_file(model, filename)

def load_data_to_table(table, filename=None, base_dir=None):
    """\
    Installs data directly into a table. Useful if table does not have a
    corresponding model, for example a many-to-many join table.
    """

    if filename is None:
        filename = _default_fixture_path_for_table(table, base_dir)
    _load_data_to_table(table, filename)

def dump_data(model, filename=None, **params):
    """\
    Dumps data to given destination. Params are optional arguments for
    selecting data.
    If ``filename`` is ``None``, assumes that destination file is located in
    :file:`fixtures/model_module_name/model_name_lowercase.yaml` of the
    application directory, e.g. :file:`MyProject/fixtures/news/newsitem.yaml.`
    """

    if filename is None:
        filename = _default_fixture_path_for_model(model)
    _dump_data_to_file(model, filename, **params)

_base_dir = os.path.dirname(os.path.dirname(__file__))

def _default_fixture_path_for_model(model, base_dir=None):
    if base_dir is None:
        base_dir = _base_dir
    path = os.path.join(base_dir, 'fixtures')
    module_dirs = model.__module__.split('.', 2)[-1].split('.')
    for dir in module_dirs:
        path = os.path.join(path, dir)
    return os.path.join(path, model.table.name + '.json')

def _default_fixture_path_for_table(table, base_dir=None):
    if base_dir is None:
        base_dir = _base_dir
    module_dirs = table.split('.')
    path = os.path.join(base_dir, 'fixtures')
    for name in module_dirs:
        path = os.path.join(path, name)
    return path + ".json"

def _is_fixture_file(filename):
    basename, ext = os.path.splitext(filename)
    return (ext.lower() in VALID_FIXTURE_FILE_EXTENSIONS)

def _load_data_from_dir(model, dirname):
    for dirpath, dirnames, filenames in os.walk(dirname):
        for filename in filenames:
            _load_data_from_file(model, filename)

def _load_data_from_file(model, filename):
    if not _is_fixture_file(filename):
        return
    fp = file(filename, 'r')
    data = simplejson.load(fp)
    fp.close()
    retval = None
    if type(data) is types.ListType:
        retval = []
        for item in data:
            retval.append(_load_instance_from_dict(model, item))
    elif type(data) is types.DictType:
        retval = {}
        for key, item in data.iteritems():
            retval[key] = _load_instance_from_dict(model, item)
    return retval

def _load_data_to_table(tablename, filename):
    if not _is_fixture_file(filename):
        return
    fp = file(filename, 'r')
    data = simplejson.load(fp)
    fp.close()
    tablename = tablename.split(".")[-1]
    table = model.context.metadata.tables[tablename]
    if type(data) is types.ListType:
        for item in data:
            table.insert(item).execute()
    elif type(data) is types.DictType:
        for key, item in data.iteritems():
            table.insert(item).execute()
    return data

def _dump_data_to_file(model, filename, **params):
    if params:
        queryset = model.select_by(**params)
    else:
        queryset = model.select()
    data = []
    for instance in queryset:
        data.append(_dump_instance_to_dict(instance))
    fp = file(filename, 'w')
    simplejson.dump(data, fp)
    fp.close()

def _load_instance_from_dict(model, dict):
    if not dict: return
    instance = model()
    fields = model._descriptor.columns.keys()
    for k, v in dict.iteritems():
        if k in fields:
            try:
                v = datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
            except:
                try:
                    v = datetime.datetime.strptime(v, '%Y-%m-%d')
                except:
                    pass
            setattr(instance, k, v)
    instance.flush()
    return instance

def _dump_instance_to_dict(instance):
    if hasattr(instance, 'to_json'):
        return instance.to_json()
    d = {}
    fields = instance._descriptor.columns.keys()
    for field in fields:
        d[field] = getattr(instance, field)
    return d

def lorem_ipsum(entity, n=10):
    from random import randint, uniform, sample, choice
    from datetime import datetime

    # constants. TODO: configurable outside?
    from pylons import config
    _storage_path = config.get('storage_path')
    _min_year = 1970
    _max_year = 2020
    _min_int = 0
    _max_int = 999999999
    _min_float = 0.0
    _max_float = 999999999.0
    _max_text = 300
    _max_paragraphs = 5
    _max_path = 64

    # cache of collections of foreign key values
    choices = {}

    try:
        # standard generator
        import lipsum
        def _text(n):
            return unicode(lipsum.Generator().generate_sentence()[:n] if n else lipsum.MarkupGenerator().generate_paragraphs_plain(randint(1, _max_paragraphs)))

    except:
        # poorman generator
        def _text(n):
            n = n or _max_text
            v = u''
            for i in xrange(randint(n/3, n)):
                v += choice(u' abcdefh gijk lmn opqr stuv wx yzABCD EFGHIJ KLMNOPQRST UVW  XYZа бвгдеё жзийк лм нопрс туфхц чшщъыь эюяАВБ ГДЕ ЁЖЗ ИЙКЛМНОП  РСТ У ФХЦЧ ШЩЪ ЫЬЭ ЮЯ 1234 567 890')
            return unicode(v)


    def _path(n):
        import os
        n = n or _max_path
        v = ''
        for i in xrange(randint(n/3, n)):
            v += choice('/abcdefhgijk/lmnopqr/stuvwxyz/ABCDEFGHIJ/KLMNOPQRST/UVW/XYZ1234567890')
        if _storage_path:
            os.makedirs(os.path.join(_storage_path, v))
        #os.close(os.open(v, os.O_WRONLY+os.O_CREAT))
        return v

    def lorem(fields):
        instance = entity()
        for f in fields:
            # don't touch primary keys. TODO: can there be many primary keys? autoincrement instead?
            if f.primary_key:
                continue
            v = 0 # reasonable default value for fields
            # analyse field type
            t = f.type.__class__.__name__
            # date
            if t in ['Date', 'DateTime']:
                m = randint(1, 12)
                d = 31 if m in [1, 3, 5, 7, 8, 10, 12] else 30
                if m == 2: d = 28 # TODO: leaps?
                v =  datetime(randint(_min_year, _max_year), m, randint(1, d), randint(0, 23), randint(0, 59), randint(0, 59))
            # boolean
            elif t == 'Boolean':
                v = randint(0, 1)
            # integer
            elif t == 'Integer':
                # foreign key -> grab possible choices from related table
                if len(f.foreign_keys) > 0:
                    table = f.foreign_keys[0].column.table
                    try:
                        v = sample(choices[table.name], 1)[0]
                    except:
                        pass
						### TODO: grab possible foreign keys from self-relating table
                        ##ids = []
                        ##for r in model.session.query(table).all():
                        ##    ids.append(r[0])
                        ##try:
                        ##    v = sample(ids, 1)[0]
                        ##except:
                        ##    pass
                # vanilla integer
                else:
                    v = randint(_min_int, _max_int)
            # float. TODO: currency subclass?
            elif t == 'Float':
                v = uniform(_min_float, _max_float)
            # path
            elif 'path' in f.name:
                n = f.type.length# or _max_text
                v = _path(n)
            # text. TODO: Char?
            elif t in ['Unicode', 'UnicodeText']:
                n = f.type.length# or _max_text
                v = _text(n)
            if not v is None:
                #print 'Setting [%s] to [%s]' % (f.name, v)
                setattr(instance, f.name, v)
        instance.flush()
        return instance

    # fetch affected fields
    fields = entity._descriptor._columns # TODO: specify excludes? but then defaults must be supplied for them!
    # grab possible keys for foreign keys from related tables
    for f in fields:
        if len(f.foreign_keys) > 0:
            table = f.foreign_keys[0].column.table
            ids = []
            for r in model.session.query(table).all():
                ids.append(r[0])
            choices[table.name] = ids

    # generate lorem-ipsum n times
    for i in xrange(n):
        lorem(fields)


def lorem_ipsum_all(n=10):
    entities = [] # enumerate your entities which you wanna be prefilled here
    for e in entities:
        lorem_ipsum(e, n)

__all__ = ['load_data', 'dump_data', 'lorem_ipsum', 'lorem_ipsum_all']
