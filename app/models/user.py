import enum
import os
import secrets
from binascii import hexlify
from typing import Union

from passlib.context import CryptContext
from tortoise import fields
from tortoise.models import Model

from app.core.models import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Roles(enum.IntEnum):

    viewer = 1
    editor = 2
    owner = 3
    admin = 4


class User(Model, BaseModel):
    role = fields.IntEnumField(Roles, default=Roles.viewer)
    login = fields.CharField(unique=True, index=True, max_length=32)
    password_hash = fields.CharField(max_length=64)
    salt = fields.CharField(max_length=32, default="", null=False)
    token = fields.CharField(max_length=32, default=lambda: secrets.token_hex(16))

    def __init__(self, *args, password, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.set_password(password)

    def set_password(self, raw_password: Union[str, bytes]) -> None:
        if isinstance(raw_password, str):
            raw_password = raw_password.encode()
        salt = hexlify(os.urandom(16))
        self.password_hash = pwd_context.hash(raw_password + salt)
        self.salt = salt.decode()

    def check_password(self, raw_password: Union[str, bytes]) -> bool:
        if isinstance(raw_password, str):
            raw_password = raw_password.encode()
        # hash_password = hexlify(pbkdf2_hmac('sha256', raw_password, self.salt.encode(), 1000))
        # return self.password_hash == hash_password.decode()
        return pwd_context.verify(raw_password + self.salt.encode(), self.password_hash)

    @property
    def first_login(self):
        return not self.salt
