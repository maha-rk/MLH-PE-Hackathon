from peewee import Model, CharField, BooleanField, DateTimeField, ForeignKeyField, IntegerField
from app.database import db
from app.models.user import User
import datetime

class URL(Model):
    user = ForeignKeyField(User, backref="urls")
    short_code = CharField(unique=True)
    original_url = CharField()
    title = CharField(null=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = db