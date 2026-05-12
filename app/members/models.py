import enum

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base


class MemberRole(str, enum.Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class Member(Base):
    __tablename__ = "members"

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    role: Mapped[MemberRole] = mapped_column(
        Enum(MemberRole),
        default=MemberRole.MEMBER
    )

    workspace = relationship("Workspace", back_populates="members")
    user = relationship("User")