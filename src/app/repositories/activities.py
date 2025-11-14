from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activities import Activity

from .base import Repository


class ActivityRepository(Repository[Activity]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Activity)

    def add(self, activity: Activity) -> None:
        super().add(activity)
