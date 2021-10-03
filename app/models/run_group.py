from tortoise import fields, Model

import app
from app.core.models import BaseModel


class RunGroup(Model, BaseModel):
    name = fields.CharField(max_length=64, null=False, unique=True)
    runs: fields.ReverseRelation["app.models.Run"]

    class Meta:
        unique_together = (("name", "deleted_at"),)
