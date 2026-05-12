# member = await get_workspace_member(
#     session=session,
#     workspace_id=workspace_id,
#     user_id=current_user.id
# )

# if not member:
#     raise HTTPException(403, "Forbidden")

import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth_dep import get_current_user
from app.dependencies.dao_dep import get_session_with_commit
from app.auth.models import User

from app.workspaces.schemas import (
    WorkspaceCreate,
    WorkspaceResponse
)

from app.workspaces.dao import WorkspacesDAO

from app.members.models import Member, MemberRole
from app.workspaces.service import WorkspaceService

router = APIRouter()


@router.get("/")
async def get_workspaces(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit)
):
    dao = WorkspacesDAO(session)

    return await dao.get_all_by_user(current_user.id)


@router.post("/")
async def create_workspace(
    data: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session_with_commit)
):
    dao = WorkspacesDAO(session)

    workspace = await dao.create({
        "name": data.name,
        "image_url": data.image_url,
        "invite_code": secrets.token_hex(3),
        "owner_id": current_user.id
    })

    member = Member(
        workspace_id=workspace.id,
        user_id=current_user.id,
        role=MemberRole.ADMIN
    )

    session.add(member)

    await session.commit()

    return workspace

@router.get("/{workspace_id}/dashboard")
async def get_workspace_dashboard(
    workspace_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user),
):
    service = WorkspaceService(session)

    data = await service.get_dashboard(workspace_id)

    return {"data": data}