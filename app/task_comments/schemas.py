from pydantic import BaseModel
from datetime import datetime
from app.tasks.models import Task

class TaskCommentCreate(BaseModel):
    content: str
    task_id: int


class TaskCommentUpdate(BaseModel):
    content: str


class TaskCommentFilter(BaseModel):
    id: int | None = None
    task_id: int | None = None