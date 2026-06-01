from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.found_clue import FoundClue
from app.schemas.found_clue import FoundClueCreate, FoundClueUpdate


class CRUDFoundClue:
    async def create(self, db: AsyncSession, *, obj_in: FoundClueCreate, lost_pet_id: UUID, reporter_id: UUID) -> FoundClue:
        db_obj = FoundClue(**obj_in.model_dump(), lost_pet_id=lost_pet_id, reporter_id=reporter_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, *, found_clue_id: UUID) -> FoundClue | None:
        result = await db.execute(
            select(FoundClue).where(FoundClue.found_clue_id == found_clue_id).options(selectinload(FoundClue.reporter))
        )
        return result.scalar_one_or_none()

    async def get_by_pet(self, db: AsyncSession, *, lost_pet_id: UUID) -> list[FoundClue]:
        result = await db.execute(
            select(FoundClue)
            .where(FoundClue.lost_pet_id == lost_pet_id)
            .options(selectinload(FoundClue.reporter))
            .order_by(FoundClue.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_reporter(self, db: AsyncSession, *, reporter_id: UUID) -> list[FoundClue]:
        result = await db.execute(
            select(FoundClue)
            .where(FoundClue.reporter_id == reporter_id)
            .order_by(FoundClue.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 20, status: str | None = None):
        from sqlalchemy import func

        query = select(FoundClue).options(selectinload(FoundClue.reporter))
        count_query = select(func.count(FoundClue.found_clue_id))

        if status:
            query = query.where(FoundClue.status == status)
            count_query = count_query.where(FoundClue.status == status)

        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(FoundClue.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all()), total

    async def update_status(self, db: AsyncSession, *, db_obj: FoundClue, obj_in: FoundClueUpdate, reviewer_id: UUID) -> FoundClue:
        db_obj.status = obj_in.status
        db_obj.admin_notes = obj_in.admin_notes
        db_obj.reviewed_by = reviewer_id
        from datetime import datetime, timezone
        db_obj.reviewed_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


crud_found_clue = CRUDFoundClue()
