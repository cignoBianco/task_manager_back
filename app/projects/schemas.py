from pydantic import BaseModel

class ProjectFilter(BaseModel):
    id: int | None = None
    workspace_id: int | None = None

class ProjectCreate(BaseModel):
    name: str
    image_url: str | None = None
    workspace_id: int


class ProjectUpdate(BaseModel):
    name: str | None = None
    image_url: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    image_url: str | None
    workspace_id: int

    class Config:
        from_attributes = True