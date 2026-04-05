from app.database import db
from .user import User
from .url import URL
from .event import Event 

def initialize_models():
    with db:
        db.create_tables([User, URL, Event])