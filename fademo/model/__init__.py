"""The application's model objects"""
import elixir
from fademo.model import meta

Session = elixir.session = meta.Session
# Uncomment if using reflected tables
# elixir.options_defaults.update({'autoload': True})
elixir.options_defaults.update({'shortnames':True})
metadata = elixir.metadata

# this will be called in config/environment.py
# if not using reflected tables
def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    metadata.bind = engine

# Delay the setup if using reflected tables
if elixir.options_defaults.get('autoload', False) \
    and not metadata.is_bound():
    elixir.delay_setup = True

# Import model entities here for convenience of referring to 
# them as model.User, model.Group, etc.

from user import *
# from upload import *
from entities import *
from demo import *

# Finally, call elixir to set up the tables.
# but not if using reflected tables
if not elixir.options_defaults.get('autoload', False):
    elixir.setup_all()
