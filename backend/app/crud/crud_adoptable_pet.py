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

    async def get(self, db: AsyncSession, *, adoptable_pet_id: UUID) -> AdoptablePet | None:
        result = await db.execute(select(AdoptablePet).where(AdoptablePet.adoptable_pet_id == adoptable_pet_id))
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
        where_clauses: list[str] = []
        params: dict[str, object] = {
            "skip": skip,
            "limit": limit,
        }

        if pet_type:
            where_clauses.append("pet_type = :pet_type")
            params["pet_type"] = pet_type

        if keyword:
            where_clauses.append(
                "(pet_name ILIKE :keyword OR breed ILIKE :keyword OR description ILIKE :keyword)"
            )
            params["keyword"] = f"%{keyword}%"

        where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

        query = text(f"""
            SELECT * FROM v_adoptable_pets
            {where_sql}
            ORDER BY intake_date DESC
            OFFSET :skip LIMIT :limit
        """)
        count_query = text(f"""
            SELECT COUNT(*) FROM v_adoptable_pets
            {where_sql}
        """)

        count_params = {key: value for key, value in params.items() if key not in {"skip", "limit"}}

        total_result = await db.execute(count_query, count_params)
        total = total_result.scalar() or 0

        result = await db.execute(query, params)
        rows = result.fetchall()
        return rows, total

    async def get_all(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 10,
    ) -> tuple[list[AdoptablePet], int]:
        count_result = await db.execute(select(func.count(AdoptablePet.adoptable_pet_id)))
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

    async def remove(self, db: AsyncSession, *, adoptable_pet_id: UUID) -> None:
        result = await db.execute(select(AdoptablePet).where(AdoptablePet.adoptable_pet_id == adoptable_pet_id))
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
