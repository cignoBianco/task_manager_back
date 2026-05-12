from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dao_dep import get_session_with_commit
from app.dependencies.auth_dep import get_current_user

from app.meetings.dao import MeetingsDAO

router = APIRouter()


@router.get("/")
async def get_meetings(
    workspace_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user)
):
    dao = MeetingsDAO(session)
    data = await dao.find_all(MeetingFilter(workspace_id=workspace_id))
    return {"data": data}