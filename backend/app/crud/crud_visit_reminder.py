from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.visit_reminder import VisitReminder
from app.schemas.visit_reminder import VisitReminderUpdate


class CRUDVisitReminder:
    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 20,
        status: str | None = None,
    ) -> tuple[list[VisitReminder], int]:
        query = select(VisitReminder)
        count_query = select(func.count(VisitReminder.reminder_id))

        if status:
            query = query.where(VisitReminder.status == status)
            count_query = count_query.where(VisitReminder.status == status)

        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(VisitReminder.reminder_date).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all()), total

    async def update(self, db: AsyncSession, *, db_obj: VisitReminder, obj_in: VisitReminderUpdate) -> VisitReminder:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def count_overdue(self, db: AsyncSession) -> int:
        from datetime import date
        result = await db.execute(
            select(func.count(VisitReminder.reminder_id)).where(
                VisitReminder.status == "pending",
                VisitReminder.reminder_date < date.today(),
            )
        )
        return result.scalar() or 0


crud_visit_reminder = CRUDVisitReminder()
