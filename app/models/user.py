from peewee import Model, CharField, DateTimeField, IntegerField
from app.database import db
import datetime

class User(Model):
    username = CharField()
    email = CharField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = db