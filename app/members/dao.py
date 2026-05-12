from app.dao.base import BaseDAO
from app.members.models import Member


class MembersDAO(BaseDAO[Member]):
    model = Member

    async def get_by_workspace(self, workspace_id: int):
        return await self.find_all(MemberFilter(workspace_id=workspace_id))