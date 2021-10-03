from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.params import Query, Path, Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.responses import Response

from app.core.view import get_current_user
from app.models import User, Test, Case, Report
from app.schema.case import CaseViewList, CaseView, CaseIn, CasePatch
from app.schema.report import ReportViewList

router = InferringRouter()


@cbv(router)
class CaseRouter:
    user: User = Depends(get_current_user)

    @router.get("/case/", response_model=CaseViewList, tags=["Case"])
    async def get_case(
        self,
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
    ):
        return {
            "items": await Case.filter(deleted_at=None).limit(limit).offset(offset).all(),
            "total": await Case.filter(deleted_at=None).count(),
        }

    @router.post("/case/", response_model=CaseView, status_code=201, tags=["Case"])
    async def create_case(self, case: CaseIn):
        test_obj = await Test.filter(id=case.test_id).get_or_none()
        if test_obj is None:
            raise HTTPException(status_code=404, detail="Test not found")
        case_obj = await Case.create(**case.dict())
        return CaseView.from_orm(case_obj)

    @router.get("/case/{case_id}/", response_model=CaseView, tags=["Case"])
    async def get_case(self, case_id: int = Path(...)):
        case_obj = await Case.filter(id=case_id, deleted_at=None).get_or_none()
        if case_obj is None:
            raise HTTPException(status_code=404, detail="Case not found")
        return CaseView.from_orm(case_obj)

    @router.patch("/case/{case_id}/", response_model=CaseView, status_code=201, tags=["Case"])
    async def patch_case(self, case_id: int = Path(...), case: CasePatch = Body(...)):
        case_obj = await Case.filter(id=case_id, deleted_at=None).get_or_none()
        if case_obj is None:
            raise HTTPException(status_code=404, detail="Case not found")

        if "test_id" in case.dict(exclude_unset=True):
            test_obj = await Test.filter(id=case.test_id).get_or_none()
            if test_obj is None:
                raise HTTPException(status_code=404, detail="Test not found")

        await case_obj.update_from_dict(case.dict(exclude_unset=True))
        await case_obj.save()
        return CaseView.from_orm(case_obj)

    @router.delete("/case/{case_id}/", status_code=201, tags=["Case"], responses={201: {"model": None}})
    async def delete_case(self, case_id: int = Path(...)):
        case_obj = await Case.filter(id=case_id, deleted_at=None).get_or_none()
        if case_obj is None:
            raise HTTPException(status_code=404, detail="Case not found")
        case_obj.deleted_at = datetime.now()
        await case_obj.save()
        return Response(status_code=201)

    @router.get("/case/{case_id}/report/", response_model=ReportViewList, tags=["Case"])
    async def get_test_case(
        self,
        case_id: int = Path(...),
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
    ):
        case_obj = await Case.filter(id=case_id, deleted_at=None).get_or_none()
        if case_obj is None:
            raise HTTPException(status_code=404, detail="Case not found")

        return {
            "items": await Report.filter(deleted_at=None, case_id=case_id).limit(limit).offset(offset).all(),
            "total": await Report.filter(deleted_at=None, case_id=case_id).count(),
        }
