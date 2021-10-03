import enum

from tortoise import fields
from tortoise.models import Model

from app.core.models import BaseModel


class ReportType(enum.IntEnum):
    system = 0
    setup = 1
    call = 2
    teardown = 3


class Report(Model, BaseModel):
    name = fields.CharField(max_length=32, default=None, null=True)
    case = fields.ForeignKeyField("models.Case", related_name="reports")
    type = fields.IntEnumField(ReportType, default=ReportType.system)
    logs: fields.ReverseRelation["Log"]
