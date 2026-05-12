from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dao_dep import get_session_with_commit
from app.dependencies.auth_dep import get_current_user

from app.tasks.dao import TasksDAO
from app.tasks.schemas import TaskCreate, TaskUpdate

router = APIRouter()


@router.get("/")
async def get_tasks(
    workspace_id: int,
    project_id: int | None = None,
    status: str | None = None,
    assignee_id: int | None = None,
    search: str | None = None,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user)
):
    dao = TasksDAO(session)
    data = await dao.get_filtered(workspace_id, project_id, status, assignee_id, search)
    return {"data": data}


@router.post("/")
async def create_task(
    data: TaskCreate,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user)
):
    dao = TasksDAO(session)
    task = await dao.add(data)
    return {"data": task}

@router.patch("/{task_id}")
async def update_task(
    task_id: int,
    data: TaskUpdate,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user),
):
    dao = TasksDAO(session)

    updated = await dao.update(
        filters=TaskFilter(id=task_id),
        values=data,
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"success": True}


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user),
):
    dao = TasksDAO(session)

    deleted = await dao.delete(TaskFilter(id=task_id))

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"success": True}