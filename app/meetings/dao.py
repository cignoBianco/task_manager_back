from app.dao.base import BaseDAO
from app.meetings.models import Meeting


class MeetingsDAO(BaseDAO[Meeting]):
    model = Meeting