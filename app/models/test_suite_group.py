from tortoise import Model, fields

import app
from app.core.models import BaseModel


class TestSuiteGroup(Model, BaseModel):
    name = fields.CharField(max_length=64, null=False)
    test_suites: fields.ReverseRelation["app.models.TestSuite"]
