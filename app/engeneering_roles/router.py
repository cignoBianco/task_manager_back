from fastapi import APIRouter, Response, Depends
from app.auth.models import User
from sqlalchemy.ext.asyncio import AsyncSession

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
async def read_category_by_query(title: str):
    role_to_return = None
    for role in ENGINEER_ROLES:
        if role.get('title').casefold() == title.casefold():
            role_to_return = role
    return role_to_return