from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.params import Query, Path, Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.responses import Response

from app.core.view import get_current_user
from app.models import User, Case, Report
from app.models.log import Log
from app.schema.log import LogViewList
from app.schema.report import ReportViewList, ReportView, ReportIn, ReportPatch

router = InferringRouter()


@cbv(router)
class ReportRouter:
    user: User = Depends(get_current_user)

    @router.get("/report/", response_model=ReportViewList, tags=["Report"])
    async def get_report(
        self,
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
    ):
        return {
            "items": await Report.filter(deleted_at=None).limit(limit).offset(offset).all(),
            "total": await Report.filter(deleted_at=None).count(),
        }

    @router.post("/report/", response_model=ReportView, status_code=201, tags=["Report"])
    async def create_report(self, report: ReportIn):
        case_obj = await Case.filter(id=report.case_id).get_or_none()
        if case_obj is None:
            raise HTTPException(status_code=404, detail="Case not found")
        report_obj = await Case.create(**report.dict())
        return ReportView.from_orm(report_obj)

    @router.get("/report/{report_id}/", response_model=ReportView, tags=["Report"])
    async def get_report(self, report_id: int = Path(...)):
        report_obj = await Report.filter(id=report_id, deleted_at=None).get_or_none()
        if report_obj is None:
            raise HTTPException(status_code=404, detail="Report not found")
        return ReportView.from_orm(report_obj)

    @router.patch("/report/{report_id}/", response_model=ReportView, status_code=201, tags=["Report"])
    async def patch_report(self, report_id: int = Path(...), report: ReportPatch = Body(...)):
        report_obj = await Report.filter(id=report_id, deleted_at=None).get_or_none()
        if report_obj is None:
            raise HTTPException(status_code=404, detail="Report not found")

        if "case_id" in report.dict(exclude_unset=True):
            case_obj = await Case.filter(id=report.case_id).get_or_none()
            if case_obj is None:
                raise HTTPException(status_code=404, detail="Case not found")

        await report_obj.update_from_dict(report.dict(exclude_unset=True))
        await report_obj.save()
        return ReportView.from_orm(report_obj)

    @router.delete("/report/{report_id}/", status_code=201, tags=["Report"], responses={201: {"model": None}})
    async def delete_report(self, report_id: int = Path(...)):
        report_obj = await Report.filter(id=report_id, deleted_at=None).get_or_none()
        if report_obj is None:
            raise HTTPException(status_code=404, detail="Report not found")
        report_obj.deleted_at = datetime.now()
        await report_obj.save()
        return Response(status_code=201)

    @router.get("/report/{report_id}/log/", response_model=LogViewList, tags=["Report"])
    async def get_report_log(
        self,
        report_id: int = Path(...),
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
    ):
        report_obj = await Report.filter(id=report_id, deleted_at=None).get_or_none()
        if report_obj is None:
            raise HTTPException(status_code=404, detail="Report not found")

        return {
            "items": await Log.filter(deleted_at=None, report_id=report_id).limit(limit).offset(offset).all(),
            "total": await Report.filter(deleted_at=None, report_id=report_id).count(),
        }
