from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, timedelta
from sqlalchemy import func, select
from app.tasks.models import Task

from app.dependencies.dao_dep import get_session_with_commit
from app.dependencies.auth_dep import get_current_user

from app.projects.dao import ProjectsDAO
from app.projects.schemas import ProjectCreate, ProjectUpdate

router = APIRouter()


@router.get("/")
async def get_projects(
    workspace_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user)
):
    dao = ProjectsDAO(session)
    data = await dao.get_by_workspace(workspace_id)
    return {"data": data}

@router.get("/{project_id}")
async def get_project(
    project_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user)
):
    dao = ProjectsDAO(session)
    project = await dao.get_by_id(project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"data": project}

@router.post("/")
async def create_project(
    data: ProjectCreate,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user)
):
    dao = ProjectsDAO(session)
    project = await dao.add(data)
    return {"data": project}

@router.patch("/{project_id}")
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user)
):
    dao = ProjectsDAO(session)

    await dao.update(
        filters=ProjectFilter(id=project_id),
        values=data
    )

    return {"data": True}

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user)
):
    dao = ProjectsDAO(session)

    deleted = await dao.delete(ProjectFilter(id=project_id))

    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")

    return {"data": True}

@router.get("/{project_id}/analytics")
async def get_project_analytics(
    project_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user),
):
    now = datetime.utcnow()
    month_ago = now - timedelta(days=30)

    # total tasks
    task_count_stmt = (
        select(func.count())
        .select_from(Task)
        .where(Task.project_id == project_id)
    )
    task_count = (await session.execute(task_count_stmt)).scalar()

    # completed
    completed_stmt = (
        select(func.count())
        .select_from(Task)
        .where(
            Task.project_id == project_id,
            Task.status == "DONE",
        )
    )
    completed_count = (await session.execute(completed_stmt)).scalar()

    # incomplete
    incomplete_stmt = (
        select(func.count())
        .select_from(Task)
        .where(
            Task.project_id == project_id,
            Task.status != "DONE",
        )
    )
    incomplete_count = (await session.execute(incomplete_stmt)).scalar()

    # overdue
    overdue_stmt = (
        select(func.count())
        .select_from(Task)
        .where(
            Task.project_id == project_id,
            Task.status != "DONE",
            Task.due_date < now,
        )
    )
    overdue_count = (await session.execute(overdue_stmt)).scalar()

    # last 30 days
    recent_stmt = (
        select(func.count())
        .select_from(Task)
        .where(
            Task.project_id == project_id,
            Task.created_at >= month_ago,
        )
    )
    recent_tasks = (await session.execute(recent_stmt)).scalar()

    return {
        "taskCount": task_count,
        "taskDifference": recent_tasks,

        "assignedTaskCount": 0,
        "assignedTaskDifference": 0,

        "completedTaskCount": completed_count,
        "completedTaskDifference": 0,

        "incompleteTaskCount": incomplete_count,
        "incompleteTaskDifference": 0,

        "overdueTaskCount": overdue_count,
        "overdueTaskDifference": 0,
    }