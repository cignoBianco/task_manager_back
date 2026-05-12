from pydantic import BaseModel


class IdFilter(BaseModel):
    id: int


class WorkspaceFilter(BaseModel):
    workspace_id: int


class ProjectFilter(BaseModel):
    id: int | None = None
    workspace_id: int | None = None


class TaskFilter(BaseModel):
    id: int | None = None
    workspace_id: int | None = None
    project_id: int | None = None
    status: str | None = None
    assignee_id: int | None = None


class MemberFilter(BaseModel):
    id: int | None = None
    workspace_id: int | None = None
    user_id: int | None = None


class TaskCommentFilter(BaseModel):
    id: int | None = None
    task_id: int | None = None


class MeetingFilter(BaseModel):
    id: int | None = None
    workspace_id: int | None = None