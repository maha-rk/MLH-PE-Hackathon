from peewee import Model, ForeignKeyField, CharField, DateTimeField
from app.database import db
from app.models.user import User
from app.models.url import URL
import datetime

class Event(Model):
    url = ForeignKeyField(URL, backref="events")
    user = ForeignKeyField(User, backref="events")
    event_type = CharField()
    timestamp = DateTimeField(default=datetime.datetime.utcnow)
    details = CharField(null=True)  # store JSON as string

    class Meta:
        database = db