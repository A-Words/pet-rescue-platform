from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review_record import ReviewRecord


class CRUDReviewRecord:
    async def create(
        self,
        db: AsyncSession,
        *,
        application_id: UUID,
        reviewer_id: UUID,
        decision: str,
        review_notes: str | None = None,
    ) -> ReviewRecord:
        db_obj = ReviewRecord(
            application_id=application_id,
            reviewer_id=reviewer_id,
            decision=decision,
            review_notes=review_notes,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


crud_review_record = CRUDReviewRecord()
