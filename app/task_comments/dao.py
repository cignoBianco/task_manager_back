from app.dao.base import BaseDAO
from app.task_comments.models import TaskComment


class TaskCommentsDAO(BaseDAO[TaskComment]):
    model = TaskComment