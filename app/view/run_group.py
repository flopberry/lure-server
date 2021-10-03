from datetime import datetime

from fastapi import Depends, Query, Path, HTTPException, Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.responses import Response

from app.core.view import get_current_user
from app.models import User, RunGroup, Run
from app.schema.run import RunViewList
from app.schema.run_group import RunGroupViewList, RunGroupView, RunGroupIn, RunGroupPatch

router = InferringRouter()


@cbv(router)
class RunGroupRouter:
    user: User = Depends(get_current_user)

    @router.get("/run-group/", response_model=RunGroupViewList, tags=["Run group"])
    async def get_run_groups(
        self,
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
    ):
        return {
            "items": await RunGroup.filter(deleted_at=None).limit(limit).offset(offset).all(),
            "total": await RunGroup.filter(deleted_at=None).all().count(),
        }

    @router.post("/run-group/", response_model=RunGroupView, status_code=201, tags=["Run group"])
    async def create_run_group(self, run_group: RunGroupIn):
        run_group_obj = await RunGroup.filter(name=run_group.name, deleted_at=None).get_or_none()
        if run_group_obj is not None:
            raise HTTPException(status_code=409, detail="Run group with this name already exists")
        run_obj = await RunGroup.create(**run_group.dict())
        return RunGroupView.from_orm(run_obj)

    @router.get("/run-group/{run_group_id}/", response_model=RunGroupView, tags=["Run group"])
    async def get_run_group(self, run_group_id: int = Path(...)):
        run_obj = await RunGroup.filter(id=run_group_id, deleted_at=None).get_or_none()
        if run_obj is None:
            raise HTTPException(status_code=404, detail="Run group not found")
        return RunGroupView.from_orm(run_obj)

    @router.get("/run-group/{run_group_id}/runs/", response_model=RunViewList, tags=["Run group"])
    async def get_run_group_runs(
        self,
        run_group_id: int = Path(...),
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
    ):
        return {
            "runs": await Run.filter(group_id=run_group_id, deleted_at=None).limit(limit).offset(offset).all(),
            "total": await Run.filter(group_id=run_group_id, deleted_at=None).count(),
        }

    @router.patch("/run-group/{run_group_id}/", response_model=RunGroupView, status_code=201, tags=["Run group"])
    async def patch_run(self, run_group_id: int = Path(...), run_group: RunGroupPatch = Body(...)):
        run_group_obj = await RunGroup.filter(id=run_group_id, deleted_at=None).get_or_none()
        if run_group_obj is None:
            raise HTTPException(status_code=404, detail="Run group not found")

        if "name" in run_group.dict(exclude_unset=True):
            run_group_obj_check = await RunGroup.filter(name=run_group.name, deleted_at=None).get_or_none()
            if run_group_obj_check is not None:
                raise HTTPException(status_code=409, detail="Run group with this name already exists")

        await run_group_obj.update_from_dict(run_group.dict(exclude_unset=True))
        await run_group_obj.save()
        return RunGroupView.from_orm(run_group_obj)

    @router.delete("/run-group/{run_group_id}/", status_code=201, tags=["Run group"], responses={201: {"model": None}})
    async def delete_run(self, run_group_id: int = Path(...)):
        run_obj = await RunGroup.filter(id=run_group_id, deleted_at=None).get_or_none()
        if run_obj is None:
            raise HTTPException(status_code=404, detail="Run group not found")
        run_obj.deleted_at = datetime.now()
        await run_obj.save()
        return Response(status_code=201)
