from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.params import Query, Path, Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.responses import Response

from app.core.view import get_current_user
from app.models import User, Report
from app.models.log import Log
from app.schema.log import LogViewList, LogIn, LogView, LogPatch
from app.schema.report import ReportView

router = InferringRouter()


@cbv(router)
class LogRouter:
    user: User = Depends(get_current_user)

    @router.get("/log/", response_model=LogViewList, tags=["Log"])
    async def get_log(
        self,
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
    ):
        return {
            "items": await Log.filter(deleted_at=None).limit(limit).offset(offset).all(),
            "total": await Log.filter(deleted_at=None).count(),
        }

    @router.post("/log/", response_model=LogView, status_code=201, tags=["Log"])
    async def create_log(self, log: LogIn):
        report_obj = await Report.filter(id=log.report_id).get_or_none()
        if report_obj is None:
            raise HTTPException(status_code=404, detail="Report not found")
        log_obj = await Log.create(**log.dict())
        return LogView.from_orm(log_obj)

    @router.get("/log/{log_id}/", response_model=LogView, tags=["Log"])
    async def get_log(self, log_id: int = Path(...)):
        log_obj = await Log.filter(id=log_id, deleted_at=None).get_or_none()
        if log_obj is None:
            raise HTTPException(status_code=404, detail="Log not found")
        return LogView.from_orm(log_obj)

    @router.patch("/log/{log_id}/", response_model=LogView, status_code=201, tags=["Log"])
    async def patch_log(self, log_id: int = Path(...), log: LogPatch = Body(...)):
        log_obj = await Log.filter(id=log_id, deleted_at=None).get_or_none()
        if log_obj is None:
            raise HTTPException(status_code=404, detail="Log not found")

        if "report_id" in log.dict(exclude_unset=True):
            report_obj = await Report.filter(id=log.report_id).get_or_none()
            if report_obj is None:
                raise HTTPException(status_code=404, detail="Log not found")

        await log_obj.update_from_dict(log.dict(exclude_unset=True))
        await log_obj.save()
        return ReportView.from_orm(log_obj)

    @router.delete("/log/{log_id}/", status_code=201, tags=["Log"], responses={201: {"model": None}})
    async def delete_log(self, log_id: int = Path(...)):
        log_obj = await Log.filter(id=log_id, deleted_at=None).get_or_none()
        if log_obj is None:
            raise HTTPException(status_code=404, detail="Log not found")
        log_obj.deleted_at = datetime.now()
        await log_obj.save()
        return Response(status_code=201)
