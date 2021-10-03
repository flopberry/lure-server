from tortoise import fields


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)


class IdMixin:
    id = fields.IntField(pk=True)


class BaseModel(IdMixin, TimestampMixin):
    pass
