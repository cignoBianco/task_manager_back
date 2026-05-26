from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dao_dep import get_session_with_commit
from app.dependencies.auth_dep import get_current_user

from app.members.dao import MembersDAO
from app.auth.models import User

from app.members.schemas import MemberFilter, MemberUpdate

router = APIRouter()


@router.get("/")
async def get_members(
    workspace_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user)
):
    dao = MembersDAO(session)
    data = await dao.find_all(MemberFilter(workspace_id=workspace_id))
    return {"data": data}

@router.delete("/{member_id}")
async def delete_member(
    member_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
    current_user: User = Depends(get_current_user),
):
    dao = MembersDAO(session)

    member = await dao.find_one_or_none(
        MemberFilter(id=member_id)
    )

    if not member:
        raise HTTPException(404, "Member not found")

    deleted = await dao.delete(
        MemberFilter(id=member_id)
    )

    return {"success": bool(deleted)}

@router.patch("/{member_id}")
async def update_member(
    member_id: int,
    data: MemberUpdate,
    session: AsyncSession = Depends(get_session_with_commit),
    current_user: User = Depends(get_current_user),
):
    dao = MembersDAO(session)

    updated = await dao.update(
        filters=MemberFilter(id=member_id),
        values=data
    )

    if not updated:
        raise HTTPException(404, "Member not found")

    return {"success": True}
