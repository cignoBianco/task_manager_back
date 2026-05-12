from pydantic import BaseModel
from datetime import datetime

class MeetingCreate(BaseModel):
    title: str
    description: str | None
    start_time: datetime
    end_time: datetime
    workspace_id: int


class MeetingUpdate(BaseModel):
    title: str | None
    description: str | None
    start_time: datetime | None
    end_time: datetime | None


class MeetingFilter(BaseModel):
    id: int | None
    workspace_id: int | None