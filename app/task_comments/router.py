from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.dao_dep import get_session_with_commit
from app.dependencies.auth_dep import get_current_user

from app.task_comments.dao import TaskCommentsDAO

router = APIRouter()


@router.get("/")
async def get_comments(
    task_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
    _=Depends(get_current_user)
):
    dao = TaskCommentsDAO(session)
    data = await dao.find_all(TaskCommentFilter(task_id=task_id))
    return {"data": data}
