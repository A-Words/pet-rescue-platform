from uuid import UUID

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.adoptable_pet import AdoptablePet
from app.schemas.adoptable_pet import AdoptablePetCreate, AdoptablePetUpdate


class CRUDAdoptablePet:
    async def create(self, db: AsyncSession, *, obj_in: AdoptablePetCreate) -> AdoptablePet:
        db_obj = AdoptablePet(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, *, id: UUID) -> AdoptablePet | None:
        result = await db.execute(select(AdoptablePet).where(AdoptablePet.id == id))
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 12,
        pet_type: str | None = None,
        keyword: str | None = None,
    ) -> tuple[list, int]:
        # Use the database view for listing available pets
        query = text("""
            SELECT * FROM v_adoptable_pets
            WHERE (:pet_type IS NULL OR pet_type = :pet_type)
              AND (:keyword IS NULL OR pet_name ILIKE :keyword OR breed ILIKE :keyword OR description ILIKE :keyword)
            ORDER BY intake_date DESC
            OFFSET :skip LIMIT :limit
        """)
        count_query = text("""
            SELECT COUNT(*) FROM v_adoptable_pets
            WHERE (:pet_type IS NULL OR pet_type = :pet_type)
              AND (:keyword IS NULL OR pet_name ILIKE :keyword OR breed ILIKE :keyword OR description ILIKE :keyword)
        """)

        keyword_pattern = f"%{keyword}%" if keyword else None

        total_result = await db.execute(count_query, {"pet_type": pet_type, "keyword": keyword_pattern})
        total = total_result.scalar() or 0

        result = await db.execute(query, {
            "pet_type": pet_type,
            "keyword": keyword_pattern,
            "skip": skip,
            "limit": limit,
        })
        rows = result.fetchall()
        return rows, total

    async def get_all(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 10,
    ) -> tuple[list[AdoptablePet], int]:
        count_result = await db.execute(select(func.count(AdoptablePet.id)))
        total = count_result.scalar() or 0

        result = await db.execute(
            select(AdoptablePet).order_by(AdoptablePet.created_at.desc()).offset(skip).limit(limit)
        )
        return list(result.scalars().all()), total

    async def update(self, db: AsyncSession, *, db_obj: AdoptablePet, obj_in: AdoptablePetUpdate) -> AdoptablePet:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: UUID) -> None:
        result = await db.execute(select(AdoptablePet).where(AdoptablePet.id == id))
        obj = result.scalar_one_or_none()
        if obj:
            await db.delete(obj)
            await db.commit()

    async def update_status(self, db: AsyncSession, *, db_obj: AdoptablePet, status: str) -> AdoptablePet:
        db_obj.adoption_status = status
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


crud_adoptable_pet = CRUDAdoptablePet()
