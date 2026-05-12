from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

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

