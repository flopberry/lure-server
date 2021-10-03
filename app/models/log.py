import enum

from tortoise import fields
from tortoise.models import Model

from app.core.models import BaseModel
from app.models import Report


class Level(enum.IntEnum):
    critical = 5
    fatal = critical
    error = 4
    warning = 3
    warn = warning
    info = 2
    debug = 1
    notset = 0


class Log(Model, BaseModel):
    name = fields.CharField(max_length=32, index=True)
    level = fields.IntEnumField(Level, default=Level.notset, index=True)
    text = fields.TextField()
    report: fields.ForeignKeyRelation[Report] = fields.ForeignKeyField("models.Report", related_name="logs")
