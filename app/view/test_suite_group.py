from datetime import datetime

from fastapi import Depends, Query, Path, HTTPException, Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.responses import Response

from app.core.view import get_current_user
from app.models import User, TestSuite, TestSuiteGroup
from app.schema.test_suite import TestSuiteView, TestSuiteIn, TestSuitePatch, TestSuiteViewList
from app.schema.test_suite_group import TestSuiteGroupViewList, TestSuiteGroupView

router = InferringRouter()


@cbv(router)
class TestSuiteGroupRouter:
    user: User = Depends(get_current_user)

    @router.get("/test-suite-group/", response_model=TestSuiteGroupViewList, tags=["Test suite group"])
    async def get_test_suite_groups(
        self,
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
    ):
        return {
            "items": await TestSuiteGroup.filter(deleted_at=None).limit(limit).offset(offset).all(),
            "total": await TestSuiteGroup.filter(deleted_at=None).count(),
        }

    @router.post("/test-suite-group/", response_model=TestSuiteGroupView, status_code=201, tags=["Test suite group"])
    async def create_test_suite_group(self, test_suite: TestSuiteIn):
        test_suite_group_obj = await TestSuiteGroup.create(**test_suite.dict())
        return TestSuiteGroupView.from_orm(test_suite_group_obj)

    @router.get(
        "/test-suite-group/{test_suite_group_id}/", response_model=TestSuiteGroupView, tags=["Test suite group"]
    )
    async def get_test_suite_group(self, test_suite_group_id: int = Path(...)):
        test_suite_group_obj = await TestSuiteGroup.filter(id=test_suite_group_id, deleted_at=None).get_or_none()
        if test_suite_group_obj is None:
            raise HTTPException(status_code=404, detail="Test suite group not found")
        return TestSuiteGroupView.from_orm(test_suite_group_obj)

    @router.patch(
        "/test-suite-group/{test_suite_group_id}/",
        response_model=TestSuiteGroupView,
        status_code=201,
        tags=["Test suite group"],
    )
    async def patch_test_suite_group(
        self, test_suite_group_id: int = Path(...), test_suite_group: TestSuitePatch = Body(...)
    ):
        test_suite_group_obj = await TestSuite.filter(id=test_suite_group_id, deleted_at=None).get_or_none()
        if test_suite_group_obj is None:
            raise HTTPException(status_code=404, detail="Test suite group not found")

        await test_suite_group_obj.update_from_dict(test_suite_group.dict(exclude_unset=True))
        await test_suite_group_obj.save()
        return TestSuiteView.from_orm(test_suite_group_obj)

    @router.delete(
        "/test-suite-group/{test_suite_group_id}/",
        status_code=201,
        tags=["Test suite group"],
        responses={201: {"model": None}},
    )
    async def delete_test_suite_group(self, test_suite_group_id: int = Path(...)):
        test_suite_group_obj = await TestSuite.filter(id=test_suite_group_id, deleted_at=None).get_or_none()
        if test_suite_group_obj is None:
            raise HTTPException(status_code=404, detail="Test suite group not found")
        test_suite_group_obj.deleted_at = datetime.now()
        await test_suite_group_obj.save()
        return Response(status_code=201)

    @router.get(
        "/test-suite-group/{test_suite_group_id}/test-suites/",
        response_model=TestSuiteViewList,
        tags=["Test suite group"],
    )
    async def get_test_suite_group_test_suites(
        self,
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
        test_suite_group_id: int = Path(...),
    ):
        test_suite_group_obj = await TestSuiteGroup.filter(id=test_suite_group_id, deleted_at=None).get_or_none()
        if test_suite_group_obj is None:
            raise HTTPException(status_code=404, detail="Test suite group not found")
        return {
            "items": await TestSuite.filter(group_id=test_suite_group_id, deleted_at=None)
            .limit(limit)
            .offset(offset)
            .all(),
            "total": TestSuite.filter(group_id=test_suite_group_id, deleted_at=None).count(),
        }
