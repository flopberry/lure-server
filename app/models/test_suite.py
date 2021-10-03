from tortoise import Model, fields

import app
from app.core.models import BaseModel


class TestSuite(Model, BaseModel):
    name = fields.CharField(max_length=64, null=False)
    group: fields.ForeignKeyRelation["app.models.TestSuiteGroup"] = fields.ForeignKeyField(
        "models.TestSuiteGroup", related_name="test_suites", null=True
    )
    run: fields.ForeignKeyRelation["app.models.Run"] = fields.ForeignKeyField("models.Run", related_name="test_suites")
