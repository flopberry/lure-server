from tortoise import fields
from tortoise.models import Model

import app
from app.core.models import BaseModel


class Run(Model, BaseModel):
    name = fields.CharField(max_length=64)
    group: fields.ForeignKeyRelation["app.models.RunGroup"] = fields.ForeignKeyField(
        "models.RunGroup", related_name="runs", null=True
    )
    test_suites: fields.ReverseRelation["app.models.TestSuite"]
