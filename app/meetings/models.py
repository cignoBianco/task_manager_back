from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.dao.database import Base


class Meeting(Base):
    __tablename__ = "meetings"

    title: Mapped[str]
    description: Mapped[str | None]

    start_time: Mapped[datetime]
    end_time: Mapped[datetime]

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE")
    )


class MeetingMember(Base):
    __tablename__ = "meeting_members"

    meeting_id: Mapped[int] = mapped_column(
        ForeignKey("meetings.id")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )