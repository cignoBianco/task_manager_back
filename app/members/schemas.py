from pydantic import BaseModel
from app.members.models import MemberRole


class MemberCreate(BaseModel):
    workspace_id: int
    user_id: int
    role: MemberRole = MemberRole.MEMBER


class MemberResponse(BaseModel):
    id: int
    workspace_id: int
    user_id: int
    role: MemberRole

    class Config:
        from_attributes = True

class MemberFilter(BaseModel):
    workspace_id: int | None = None
    id: int | None = None

class MemberUpdate(BaseModel):
    role: MemberRole