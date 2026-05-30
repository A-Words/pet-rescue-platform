from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_lost_pet import crud_lost_pet
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.lost_pet import LostPetCreate, LostPetResponse, LostPetUpdate

router = APIRouter()


@router.post("", response_model=LostPetResponse, status_code=status.HTTP_201_CREATED)
async def create_lost_pet(
    obj_in: LostPetCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pet = await crud_lost_pet.create(db, obj_in=obj_in, user_id=current_user.id)
    return pet


@router.get("", response_model=dict)
async def list_lost_pets(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    pet_type: str | None = None,
    status: str | None = None,
    keyword: str | None = None,
):
    skip = (page - 1) * page_size
    items, total = await crud_lost_pet.get_multi(
        db, skip=skip, limit=page_size, pet_type=pet_type, status=status, keyword=keyword
    )
    return {
        "items": [LostPetResponse.model_validate(p) for p in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/my", response_model=list[LostPetResponse])
async def my_lost_pets(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await crud_lost_pet.get_by_user(db, user_id=current_user.id)


@router.get("/{pet_id}", response_model=LostPetResponse)
async def get_lost_pet(pet_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    pet = await crud_lost_pet.get(db, id=pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.put("/{pet_id}", response_model=LostPetResponse)
async def update_lost_pet(
    pet_id: UUID,
    obj_in: LostPetUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pet = await crud_lost_pet.get(db, id=pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    if pet.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return await crud_lost_pet.update(db, db_obj=pet, obj_in=obj_in)


@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lost_pet(
    pet_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pet = await crud_lost_pet.get(db, id=pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    if pet.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    await crud_lost_pet.remove(db, id=pet_id)


@router.patch("/{pet_id}/status", response_model=LostPetResponse)
async def update_lost_pet_status(
    pet_id: UUID,
    body: dict,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pet = await crud_lost_pet.get(db, id=pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    if pet.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    new_status = body.get("status")
    if new_status not in ("active", "found", "closed"):
        raise HTTPException(status_code=400, detail="Invalid status")
    return await crud_lost_pet.update(db, db_obj=pet, obj_in=LostPetUpdate(status=new_status))
