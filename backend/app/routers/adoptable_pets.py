from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_adoptable_pet import crud_adoptable_pet
from app.dependencies import get_db, require_admin
from app.models.user import User
from app.schemas.adoptable_pet import AdoptablePetCreate, AdoptablePetResponse, AdoptablePetUpdate

router = APIRouter()


@router.post("", response_model=AdoptablePetResponse, status_code=status.HTTP_201_CREATED)
async def create_adoptable_pet(
    obj_in: AdoptablePetCreate,
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await crud_adoptable_pet.create(db, obj_in=obj_in)


@router.get("", response_model=dict)
async def list_adoptable_pets(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    pet_type: str | None = None,
    keyword: str | None = None,
):
    skip = (page - 1) * page_size
    items, total = await crud_adoptable_pet.get_multi(
        db, skip=skip, limit=page_size, pet_type=pet_type, keyword=keyword
    )
    # Convert view rows to response-like dicts
    result_items = []
    for row in items:
        result_items.append({
            "adoptable_pet_id": row.adoptable_pet_id,
            "pet_name": row.pet_name,
            "pet_type": row.pet_type,
            "breed": row.breed,
            "color": row.color,
            "gender": row.gender,
            "age_months": row.age_months,
            "photo_urls": row.photo_urls,
            "description": row.description,
            "health_status": row.health_status,
            "is_vaccinated": row.is_vaccinated,
            "is_dewormed": row.is_dewormed,
            "is_sterilized": row.is_sterilized,
            "adoption_status": "available",
            "rescue_station": row.rescue_station,
            "intake_date": str(row.intake_date),
            "application_count": row.application_count,
            "created_at": None,
            "updated_at": None,
        })
    return {"items": result_items, "total": total, "page": page, "page_size": page_size}


@router.get("/{adoptable_pet_id}", response_model=AdoptablePetResponse)
async def get_adoptable_pet(adoptable_pet_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    pet = await crud_adoptable_pet.get(db, adoptable_pet_id=adoptable_pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.put("/{adoptable_pet_id}", response_model=AdoptablePetResponse)
async def update_adoptable_pet(
    adoptable_pet_id: UUID,
    obj_in: AdoptablePetUpdate,
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pet = await crud_adoptable_pet.get(db, adoptable_pet_id=adoptable_pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return await crud_adoptable_pet.update(db, db_obj=pet, obj_in=obj_in)


@router.delete("/{adoptable_pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_adoptable_pet(
    adoptable_pet_id: UUID,
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pet = await crud_adoptable_pet.get(db, adoptable_pet_id=adoptable_pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    await crud_adoptable_pet.remove(db, adoptable_pet_id=adoptable_pet_id)


@router.patch("/{adoptable_pet_id}/status", response_model=AdoptablePetResponse)
async def update_adoption_status(
    adoptable_pet_id: UUID,
    body: dict,
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pet = await crud_adoptable_pet.get(db, adoptable_pet_id=adoptable_pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    new_status = body.get("status")
    if new_status not in ("available", "reserved", "adopted"):
        raise HTTPException(status_code=400, detail="Invalid status")
    return await crud_adoptable_pet.update_status(db, db_obj=pet, status=new_status)
