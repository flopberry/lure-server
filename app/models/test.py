from tortoise import Model, fields

import app
from app.core.models import BaseModel


class Test(Model, BaseModel):
    name = fields.CharField(max_length=256)
    test_suite: fields.ForeignKeyRelation["app.models.TestSuite"] = fields.ForeignKeyField(
        "models.TestSuite", related_name="tests"
    )
    cases: fields.ReverseRelation["app.models.Case"]
