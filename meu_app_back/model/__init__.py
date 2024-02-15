from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Import elements defined in the model
from model.base import Base
from model.comment import Comment
from model.company import Company

db_path = "database/"
# Check if the directory does not exist
if not os.path.exists(db_path):
   # If it doesn't exist, create the directory
   os.makedirs(db_path)

# Database access URL (this is a URL for local sqlite access)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# Create the connection engine to the database
engine = create_engine(db_url, echo=False)

# Instantiate a session creator with the database
Session = sessionmaker(bind=engine)

# Create the database if it does not exist
if not database_exists(engine.url):
    create_database(engine.url) 

# Create the database tables if they do not exist
Base.metadata.create_all(engine)
