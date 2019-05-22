from peewee import *
import os
from playhouse.db_url import connect


db = connect(os.environ.get('DATABASE_URL'))


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    uid = IntegerField(unique=True)


class Place(BaseModel, Model):
    title = CharField()
    address = CharField()
    latitude = DecimalField()
    longitude = DecimalField()
    user = ForeignKeyField(User)