from sqlalchemy import select
from app.tasks.models import Task
from app.projects.models import Project
from app.members.models import Member


class WorkspaceService:
    def __init__(self, session):
        self.session = session

    async def get_dashboard(self, workspace_id: int):
        tasks = await self.session.execute(
            select(Task).where(Task.workspace_id == workspace_id)
        )

        projects = await self.session.execute(
            select(Project).where(Project.workspace_id == workspace_id)
        )

        members = await self.session.execute(
            select(Member).where(Member.workspace_id == workspace_id)
        )

        return {
            "tasks": tasks.scalars().all(),
            "projects": projects.scalars().all(),
            "members": members.scalars().all(),
        }