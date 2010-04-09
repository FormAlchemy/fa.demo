"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

__all__ = ['Session', 'metadata']

# SQLAlchemy database engine.  Updated by model.init_model()
engine = None

# Ready for SQLA 0.5 where autoflush defaults to True
# and autocommit defaults to False (see SQLA sessionmaker 
# docs for details of alternative configurations)

# SQLAlchemy session manager.  Updated by model.init_model()
import sqlalchemy
if sqlalchemy.__version__ > '0.5':
    Session = scoped_session(sessionmaker())
else:
    Session = scoped_session(sessionmaker(autoflush=True, transactional=True))

# Global metadata. If you have multiple databases with overlapping table
# names, you'll need a metadata for each database
metadata = MetaData()
