from sqlalchemy import select

from app.members.models import Member


async def get_workspace_member(
    session,
    workspace_id,
    user_id
):
    query = select(Member).where(
        Member.workspace_id == workspace_id,
        Member.user_id == user_id
    )

    result = await session.execute(query)

    return result.scalar_one_or_none()