from fastapi import APIRouter, Response, Depends
from app.auth.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.auth_dep import get_current_user, get_current_admin_user, check_refresh_token
from app.dependencies.dao_dep import get_session_with_commit, get_session_without_commit

router = APIRouter()


ENGINEER_ROLES = [
    {'title': 'Frontend Developer', 'mainskill': 'React'},
    {'title': 'Backend Developer', 'mainskill': 'Node.js'},
    {'title': 'Fullstack Developer', 'mainskill': 'Next.js'},
    {'title': 'Machine Learning Engineer', 'mainskill': 'Tensorflow'},
    {'title': 'Data Scientist', 'mainskill': 'Apache Spark'},
    {'title': 'Software Architect', 'mainskill': 'System Analysis'},
]

@router.get("/")
async def read_category_by_query(title: str, session: AsyncSession = Depends(get_session_with_commit),
                        user_data: User = Depends(get_current_admin_user)):
    role_to_return = None
    for role in ENGINEER_ROLES:
        if role.get('title').casefold() == title.casefold():
            role_to_return = role
    return role_to_return