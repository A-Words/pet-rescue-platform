from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.lost_pet import LostPet
from app.schemas.lost_pet import LostPetCreate, LostPetUpdate


class CRUDLostPet:
    async def create(self, db: AsyncSession, *, obj_in: LostPetCreate, user_id: UUID) -> LostPet:
        db_obj = LostPet(**obj_in.model_dump(), user_id=user_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, *, id: UUID) -> LostPet | None:
        result = await db.execute(
            select(LostPet).where(LostPet.id == id).options(selectinload(LostPet.user))
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 12,
        pet_type: str | None = None,
        status: str | None = None,
        keyword: str | None = None,
    ) -> tuple[list[LostPet], int]:
        query = select(LostPet).options(selectinload(LostPet.user))
        count_query = select(func.count(LostPet.id))

        if pet_type:
            query = query.where(LostPet.pet_type == pet_type)
            count_query = count_query.where(LostPet.pet_type == pet_type)
        if status:
            query = query.where(LostPet.status == status)
            count_query = count_query.where(LostPet.status == status)
        if keyword:
            pattern = f"%{keyword}%"
            cond = LostPet.pet_name.ilike(pattern) | LostPet.breed.ilike(pattern) | LostPet.description.ilike(pattern)
            query = query.where(cond)
            count_query = count_query.where(cond)

        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(LostPet.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all()), total

    async def update(self, db: AsyncSession, *, db_obj: LostPet, obj_in: LostPetUpdate) -> LostPet:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: UUID) -> None:
        result = await db.execute(select(LostPet).where(LostPet.id == id))
        obj = result.scalar_one_or_none()
        if obj:
            await db.delete(obj)
            await db.commit()

    async def get_by_user(self, db: AsyncSession, *, user_id: UUID) -> list[LostPet]:
        result = await db.execute(
            select(LostPet)
            .where(LostPet.user_id == user_id)
            .options(selectinload(LostPet.user))
            .order_by(LostPet.created_at.desc())
        )
        return list(result.scalars().all())


crud_lost_pet = CRUDLostPet()
