from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.adoption_application import AdoptionApplication
from app.schemas.adoption_application import AdoptionApplicationCreate


class CRUDAdoptionApplication:
    async def create(self, db: AsyncSession, *, obj_in: AdoptionApplicationCreate, applicant_id: UUID) -> AdoptionApplication:
        db_obj = AdoptionApplication(**obj_in.model_dump(), applicant_id=applicant_id)
        db.add(db_obj)
        await db.flush()
        application_id = db_obj.application_id
        await db.commit()
        created = await self.get(db, application_id=application_id)
        if created is None:
            raise RuntimeError("Created adoption application not found")
        return created

    async def get(self, db: AsyncSession, *, application_id: UUID) -> AdoptionApplication | None:
        result = await db.execute(
            select(AdoptionApplication)
            .where(AdoptionApplication.application_id == application_id)
            .options(
                selectinload(AdoptionApplication.pet),
                selectinload(AdoptionApplication.review_records),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_applicant(self, db: AsyncSession, *, applicant_id: UUID) -> list[AdoptionApplication]:
        result = await db.execute(
            select(AdoptionApplication)
            .where(AdoptionApplication.applicant_id == applicant_id)
            .options(
                selectinload(AdoptionApplication.pet),
                selectinload(AdoptionApplication.review_records),
            )
            .order_by(AdoptionApplication.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 20,
        status: str | None = None,
    ) -> tuple[list[AdoptionApplication], int]:
        query = select(AdoptionApplication).options(
            selectinload(AdoptionApplication.pet),
            selectinload(AdoptionApplication.review_records),
        )
        count_query = select(func.count(AdoptionApplication.application_id))

        if status:
            query = query.where(AdoptionApplication.status == status)
            count_query = count_query.where(AdoptionApplication.status == status)

        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(AdoptionApplication.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all()), total

    async def cancel(self, db: AsyncSession, *, db_obj: AdoptionApplication) -> AdoptionApplication:
        db_obj.status = "cancelled"
        application_id = db_obj.application_id
        await db.commit()
        cancelled = await self.get(db, application_id=application_id)
        if cancelled is None:
            raise RuntimeError("Cancelled adoption application not found")
        return cancelled


crud_adoption_application = CRUDAdoptionApplication()
