from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dao_dep import get_session_with_commit
from app.dependencies.auth_dep import get_current_user

from app.members.dao import MembersDAO

from app.members.schemas import MemberFilter

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