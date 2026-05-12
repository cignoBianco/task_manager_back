from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.workspaces.models import Workspace
from app.members.models import Member


class WorkspacesDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict):
        workspace = Workspace(**data)

        self.session.add(workspace)

        await self.session.flush()

        return workspace

    async def get_by_id(self, workspace_id: int):
        query = select(Workspace).where(
            Workspace.id == workspace_id
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def get_all_by_user(self, user_id: int):
        stmt = (
            select(Workspace)
            .join(Member, Member.workspace_id == Workspace.id)
            .where(Member.user_id == user_id)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    
        # MEMBERS
        members_stmt = select(Member).where(Member.workspace_id == workspace_id)
        members = (await self._session.execute(members_stmt)).scalars().all()

        # ANALYTICS
        tasks_total = len(tasks)
        tasks_done = len([t for t in tasks if t.status == "DONE"])
        tasks_in_progress = len([t for t in tasks if t.status == "IN_PROGRESS"])

        return {
            "analytics": {
                "tasks_total": tasks_total,
                "tasks_done": tasks_done,
                "tasks_in_progress": tasks_in_progress,
                "projects_total": len(projects),
                "members_total": len(members),
            },
            "tasks": tasks,
            "projects": projects,
            "members": members,
        }