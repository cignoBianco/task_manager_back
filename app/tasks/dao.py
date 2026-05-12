from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.models import Task


class TasksDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict):
        task = Task(**data)
        self.session.add(task)
        await self.session.flush()
        return task

    async def get_by_id(self, task_id: int):
        res = await self.session.execute(
            select(Task).where(Task.id == task_id)
        )
        return res.scalar_one_or_none()

    async def get_all(self, filters: dict):
        query = select(Task)

        if filters.get("workspace_id"):
            query = query.where(Task.workspace_id == filters["workspace_id"])

        if filters.get("project_id"):
            query = query.where(Task.project_id == filters["project_id"])

        if filters.get("status"):
            query = query.where(Task.status == filters["status"])

        if filters.get("assignee_id"):
            query = query.where(Task.assignee_id == filters["assignee_id"])

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_filtered(
        self,
        workspace_id: int,
        project_id: int | None = None,
        status: str | None = None,
        assignee_id: int | None = None,
        search: str | None = None,
    ):
        # filters = type("F", (), {
        #     "workspace_id": workspace_id,
        #     "project_id": project_id,
        #     "status": status,
        #     "assignee_id": assignee_id,
        #     "search": search,
        # })()

        return await self.get_all({
            "workspace_id": workspace_id,
            "project_id": project_id,
            "status": status,
            "assignee_id": assignee_id,
        })

    async def get_by_workspace(self, workspace_id: int):
        from app.schemas.common_filters import TaskFilter
        return await self.get_all(TaskFilter(workspace_id=workspace_id))