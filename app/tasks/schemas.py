from pydantic import BaseModel
from datetime import datetime
from app.tasks.models import TaskStatus


class TaskCreate(BaseModel):
    name: str
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    position: int
    due_date: datetime
    workspace_id: int
    project_id: int
    assignee_id: int


class TaskFilter(BaseModel):
    id: int | None = None
    workspace_id: int | None = None
    project_id: int | None = None
    status: TaskStatus | None = None

class TaskUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    position: int | None = None
    due_date: datetime | None = None
    assignee_id: int | None = None


class TaskResponse(BaseModel):
    id: int
    name: str
    description: str | None
    status: TaskStatus
    position: int
    due_date: datetime
    workspace_id: int
    project_id: int
    assignee_id: int

    class Config:
        from_attributes = True