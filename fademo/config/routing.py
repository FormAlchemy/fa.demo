"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper
from formalchemy.ext.pylons import maps # routes generator

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    # Map the /admin url to FA's AdminController
    # Map static files
    map.connect('fa_static', '/jquery/{path_info:.*}', controller='jquery')
    # Uploads
    map.connect('upload', '/upload', controller='upload')
    map.connect('upload', '/upload/{path_info:.*}', controller='upload')
    # Index page
    map.connect('admin', '/', controller='admin', action='models')
    # Models
    map.resource('model', 'models', path_prefix='/{model_name}', controller='admin')

    return map
