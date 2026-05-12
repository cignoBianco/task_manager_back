from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base


class Project(Base):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255))
    image_url: Mapped[str | None]

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE")
    )

    workspace = relationship("Workspace", back_populates="projects")

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan"
    )