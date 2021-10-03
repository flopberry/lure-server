from datetime import datetime

from fastapi import Path, Query, HTTPException, Depends, Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.responses import Response

from app.core.view import get_current_user
from app.models import Run, User, RunGroup
from app.schema.run import RunIn, RunView, RunViewList, RunPatch

router = InferringRouter()


@cbv(router)
class RunRouter:
    user: User = Depends(get_current_user)

    @router.get("/run/", response_model=RunViewList, tags=["Run"])
    async def get_runs(
        self,
        limit: int = Query(default=10, ge=0, le=100),
        offset: int = Query(default=0),
    ):
        return {
            "items": await Run.filter(deleted_at=None).limit(limit).offset(offset).all(),
            "total": await Run.filter(deleted_at=None).count(),
        }

    @router.post("/run/", response_model=RunView, status_code=201, tags=["Run"])
    async def create_run(self, run: RunIn):
        run_obj = await Run.create(**run.dict())
        return RunView.from_orm(run_obj)

    @router.get("/run/{run_id}/", response_model=RunView, tags=["Run"])
    async def get_run(self, run_id: int = Path(...)):
        run_obj = await Run.filter(id=run_id, deleted_at=None).get_or_none()
        if run_obj is None:
            raise HTTPException(status_code=404, detail="Run not found")
        return RunView.from_orm(run_obj)

    @router.patch("/run/{run_id}/", response_model=RunView, status_code=201, tags=["Run"])
    async def patch_run(self, run_id: int = Path(...), run: RunPatch = Body(...)):
        run_obj = await Run.filter(id=run_id, deleted_at=None).get_or_none()
        if run_obj is None:
            raise HTTPException(status_code=404, detail="Run not found")
        if "group_id" in run.dict(exclude_unset=True):
            run_group_obj = await RunGroup.filter(id=run.group_id, deleted_at=None).get_or_none()
            if run_group_obj is None:
                raise HTTPException(status_code=404, detail="Run group not found")
        await run_obj.update_from_dict(run.dict(exclude_unset=True))
        await run_obj.save()
        return RunView.from_orm(run_obj)

    @router.delete("/run/{run_id}/", status_code=201, tags=["Run"], responses={201: {"model": None}})
    async def delete_run(self, run_id: int = Path(...)):
        run_obj = await Run.filter(id=run_id, deleted_at=None).get_or_none()
        if run_obj is None:
            raise HTTPException(status_code=404, detail="Run not found")
        run_obj.deleted_at = datetime.now()
        await run_obj.save()
        return Response(status_code=201)
