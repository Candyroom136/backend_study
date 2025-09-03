from tortoise.models import Model
from tortoise.fields import IntField, CharField, DatetimeField
from datetime import datetime

class User(Model):
    id = IntField(primary_key=True)
    name = CharField(max_length=100)
    email = CharField(max_length=100, unique=True)
    created_at = DatetimeField(default=datetime.now)
    
    class Meta:
        table = "users"