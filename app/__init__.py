import logging

from fastapi import FastAPI

from app.view.run import router as run_router
from app.view.run_group import router as run_group_router
from app.view.test_suite import router as test_suite_router
from app.view.test_suite_group import router as test_suite_group_router
from app.view.test import router as test_router
from app.view.case import router as case_router
from app.view.report import router as report_router
from app.view.log import router as log_router
from app.view.user import router as user_router
from .models import init_db

log = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI(title="Lure", version="0.0.1", redoc_url=None)
    init_db(application)
    application.include_router(user_router)
    application.include_router(run_router)
    application.include_router(run_group_router)
    application.include_router(test_suite_router)
    application.include_router(test_suite_group_router)
    application.include_router(test_router)
    application.include_router(case_router)
    application.include_router(report_router)
    application.include_router(log_router)
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    print("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
