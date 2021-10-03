from datetime import datetime

from fastapi import Depends, Query, Path, HTTPException, Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.responses import Response

from app.core.view import get_current_user
from app.models import User, Run, TestSuite, TestSuiteGroup, Test
from app.schema.test import TestViewList
from app.schema.test_suite import TestSuiteViewList, TestSuiteView, TestSuiteIn, TestSuitePatch

router = InferringRouter()


@cbv(router)
class TestSuiteRouter:
    user: User = Depends(get_current_user)

    @router.get("/test-suite/", response_model=TestSuiteViewList, tags=["Test suite"])
    async def get_test_suites(
        self,
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
    ):
        return {
            "items": await TestSuite.filter(deleted_at=None).limit(limit).offset(offset).all(),
            "total": await TestSuite.filter(deleted_at=None).count(),
        }

    @router.post("/test-suite/", response_model=TestSuiteView, status_code=201, tags=["Test suite"])
    async def create_test_suite(self, test_suite: TestSuiteIn):
        run_obj = await Run.filter(id=test_suite.run_id).get_or_none()
        if run_obj is None:
            raise HTTPException(status_code=404, detail="Run not found")

        if "group_id" in test_suite.dict(exclude_unset=True):
            group_obj = await TestSuiteGroup.filter(id=test_suite.group_id).get_or_none()
            if group_obj is None:
                raise HTTPException(status_code=404, detail="Test suite group not found")

        test_suite_obj = await TestSuite.create(**test_suite.dict())
        return TestSuiteView.from_orm(test_suite_obj)

    @router.get("/test-suite/{test_suite_id}/", response_model=TestSuiteView, tags=["Test suite"])
    async def get_test_suite(self, test_suite_id: int = Path(...)):
        test_suite_obj = await TestSuite.filter(id=test_suite_id, deleted_at=None).get_or_none()
        if test_suite_obj is None:
            raise HTTPException(status_code=404, detail="Test suite not found")
        return TestSuiteView.from_orm(test_suite_obj)

    @router.patch("/test-suite/{test_suite_id}/", response_model=TestSuiteView, status_code=201, tags=["Test suite"])
    async def patch_test_suite(self, test_suite_id: int = Path(...), test_suite: TestSuitePatch = Body(...)):
        test_suite_obj = await TestSuite.filter(id=test_suite_id, deleted_at=None).get_or_none()
        if test_suite_obj is None:
            raise HTTPException(status_code=404, detail="Test suite not found")

        if "run_id" in test_suite.dict(exclude_unset=True):
            run_obj = await Run.filter(id=test_suite.run_id).get_or_none()
            if run_obj is None:
                raise HTTPException(status_code=404, detail="Run not found")

        if "group_id" in test_suite.dict(exclude_unset=True):
            test_suite_obj = await TestSuiteGroup.filter(id=test_suite.group_id, deleted_at=None).get_or_none()
            if test_suite_obj is None:
                raise HTTPException(status_code=404, detail="Test suite group not found")
        await test_suite_obj.update_from_dict(test_suite.dict(exclude_unset=True))
        await test_suite_obj.save()
        return TestSuiteView.from_orm(test_suite_obj)

    @router.delete(
        "/test-suite/{test_suite_id}/", status_code=201, tags=["Test suite"], responses={201: {"model": None}}
    )
    async def delete_test_suite(self, test_suite_id: int = Path(...)):
        test_suite_obj = await TestSuite.filter(id=test_suite_id, deleted_at=None).get_or_none()
        if test_suite_obj is None:
            raise HTTPException(status_code=404, detail="Test suite not found")
        test_suite_obj.deleted_at = datetime.now()
        await test_suite_obj.save()
        return Response(status_code=201)

    @router.get("/test-suite/{test_suite_id}/test/", response_model=TestViewList, tags=["Test suite"])
    async def get_test_suite(
        self,
        test_suite_id: int = Path(...),
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
    ):
        test_suite_obj = await TestSuite.filter(id=test_suite_id, deleted_at=None).get_or_none()
        if test_suite_obj is None:
            raise HTTPException(status_code=404, detail="Test suite not found")

        return {
            "items": await Test.filter(deleted_at=None, test_suite_id=test_suite_id).limit(limit).offset(offset).all(),
            "total": await Test.filter(deleted_at=None, test_suite_id=test_suite_id).count(),
        }
