from app.dao.base import BaseDAO
from app.projects.models import Project

from app.projects.schemas import ProjectFilter, ProjectUpdate


class ProjectsDAO(BaseDAO[Project]):
    model = Project

    async def get_by_workspace(self, workspace_id: int):
        return await self.find_all(
            filters=ProjectFilter(workspace_id=workspace_id)
        )