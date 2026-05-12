from pydantic import BaseModel
from app.projects.schemas import ProjectResponse
from app.tasks.schemas import TaskResponse
from app.members.schemas import MemberResponse



class WorkspaceCreate(BaseModel):
    name: str
    image_url: str | None = None


class WorkspaceUpdate(BaseModel):
    name: str
    image_url: str | None = None


class WorkspaceResponse(BaseModel):
    id: int
    name: str
    image_url: str | None
    invite_code: str

    class Config:
        from_attributes = True


class WorkspaceAnalytics(BaseModel):
    tasks_total: int
    tasks_done: int
    tasks_in_progress: int
    projects_total: int
    members_total: int

class WorkspaceDashboard(BaseModel):
    analytics: WorkspaceAnalytics
    tasks: list[TaskResponse]
    projects: list[ProjectResponse]
    members: list[MemberResponse]