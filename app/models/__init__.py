from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app import constants
from .case import Case
from .report import Report
from .run import Run
from .run_group import RunGroup
from .test import Test
from .test_suite import TestSuite
from .test_suite_group import TestSuiteGroup
from .user import User

TORTOISE_ORM = {
    "connections": {"default": constants.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app=app,
        db_url=constants.DATABASE_URL,
        modules={"models": ["app.models", "aerich.models"]},
        generate_schemas=False,
        add_exception_handlers=False,
    )
