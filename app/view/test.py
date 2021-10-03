from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.params import Query, Path, Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.responses import Response

from app.core.view import get_current_user
from app.models import User, Test, TestSuite, Case
from app.schema.test import TestViewList, TestView, TestIn, TestPatch

router = InferringRouter()


@cbv(router)
class TestRouter:
    user: User = Depends(get_current_user)

    @router.get("/test/", response_model=TestViewList, tags=["Test"])
    async def get_test(
        self,
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
    ):
        return {
            "items": await Test.filter(deleted_at=None).limit(limit).offset(offset).all(),
            "total": await Test.filter(deleted_at=None).count(),
        }

    @router.post("/test/", response_model=TestView, status_code=201, tags=["Test"])
    async def create_test(self, test: TestIn):
        test_suite_obj = await TestSuite.filter(id=test.test_suite_id).get_or_none()
        if test_suite_obj is None:
            raise HTTPException(status_code=404, detail="Test suite not found")
        test_obj = await Test.create(**test.dict())
        return TestView.from_orm(test_obj)

    @router.get("/test/{test_id}/", response_model=TestView, tags=["Test"])
    async def get_test(self, test_id: int = Path(...)):
        test_obj = await Test.filter(id=test_id, deleted_at=None).get_or_none()
        if test_obj is None:
            raise HTTPException(status_code=404, detail="Test not found")
        return TestView.from_orm(test_obj)

    @router.patch("/test/{test_id}/", response_model=TestView, status_code=201, tags=["Test"])
    async def patch_test(self, test_id: int = Path(...), test: TestPatch = Body(...)):
        test_obj = await Test.filter(id=test_id, deleted_at=None).get_or_none()
        if test_obj is None:
            raise HTTPException(status_code=404, detail="Test not found")

        if "test_suite_id" in test.dict(exclude_unset=True):
            test_suite_obj = await TestSuite.filter(id=test.test_suite_id).get_or_none()
            if test_suite_obj is None:
                raise HTTPException(status_code=404, detail="Test suite not found")

        await test_obj.update_from_dict(test.dict(exclude_unset=True))
        await test_obj.save()
        return TestView.from_orm(test_obj)

    @router.delete(
        "/test/{test_id}/", status_code=201, tags=["Test"], responses={201: {"model": None}}
    )
    async def delete_test(self, test_id: int = Path(...)):
        test_obj = await Test.filter(id=test_id, deleted_at=None).get_or_none()
        if test_obj is None:
            raise HTTPException(status_code=404, detail="Test not found")
        test_obj.deleted_at = datetime.now()
        await test_obj.save()
        return Response(status_code=201)

    @router.get("/test/{test_id}/case/", response_model=TestViewList, tags=["Test"])
    async def get_test_case(
        self,
        test_id: int = Path(...),
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
    ):
        test_obj = await Test.filter(id=test_id, deleted_at=None).get_or_none()
        if test_obj is None:
            raise HTTPException(status_code=404, detail="Test not found")

        return {
            "items": await Case.filter(deleted_at=None, test_id=test_id).limit(limit).offset(offset).all(),
            "total": await Test.filter(deleted_at=None, test_id=test_id).count(),
        }
