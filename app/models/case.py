import enum

from tortoise import Model, fields

import app
from app.core.models import BaseModel


class Statuses(enum.IntEnum):
    passed = 1
    failed = 2
    error = 3
    skipped = 4
    progress = 5
    pending = 6


class Case(Model, BaseModel):
    name = fields.CharField(max_length=128)
    status = fields.IntEnumField(Statuses, default=Statuses.pending)
    test: fields.ForeignKeyRelation['app.models.Test'] = fields.ForeignKeyField("models.Test", related_name="cases")
