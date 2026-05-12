from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    name: Mapped[str] = mapped_column(String(255))
    image_url: Mapped[str | None]
    invite_code: Mapped[str]

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    owner = relationship("User")

    projects = relationship(
        "Project",
        back_populates="workspace",
        cascade="all, delete-orphan"
    )

    members = relationship(
        "Member",
        back_populates="workspace",
        cascade="all, delete-orphan"
    )