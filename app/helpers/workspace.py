from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.members.dao import MemberDAO

async def get_workspace_member(session: AsyncSession, workspace_id: int, user_id: int):
    member = await MemberDAO(session).find_one_or_none_by_filters(
        workspace_id=workspace_id,
        user_id=user_id
    )

    if not member:
        raise HTTPException(status_code=403, detail="No access to workspace")

    return member