import enum
from datetime import datetime

from sqlalchemy import String, ForeignKey, Enum, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base


class TaskStatus(str, enum.Enum):
    BACKLOG = "BACKLOG"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    IN_REVIEW = "IN_REVIEW"
    DONE = "DONE"


class Task(Base):
    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column(String(255))

    description: Mapped[str | None] = mapped_column(Text)

    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.TODO
    )

    position: Mapped[int] = mapped_column(Integer)

    due_date: Mapped[datetime]

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE")
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )

    assignee_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    project = relationship("Project", back_populates="tasks")