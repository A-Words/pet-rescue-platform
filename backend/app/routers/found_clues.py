from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_found_clue import crud_found_clue
from app.crud.crud_lost_pet import crud_lost_pet
from app.dependencies import get_current_user, require_admin, get_db
from app.models.user import User
from app.schemas.found_clue import FoundClueCreate, FoundClueResponse, FoundClueUpdate

router = APIRouter()


@router.post("/lost-pets/{pet_id}/clues", response_model=FoundClueResponse, status_code=status.HTTP_201_CREATED)
async def submit_clue(
    pet_id: UUID,
    obj_in: FoundClueCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pet = await crud_lost_pet.get(db, id=pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    clue = await crud_found_clue.create(db, obj_in=obj_in, lost_pet_id=pet_id, reporter_id=current_user.id)
    return clue


@router.get("/lost-pets/{pet_id}/clues", response_model=list[FoundClueResponse])
async def list_clues_for_pet(
    pet_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pet = await crud_lost_pet.get(db, id=pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    if pet.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return await crud_found_clue.get_by_pet(db, lost_pet_id=pet_id)


@router.get("/my", response_model=list[FoundClueResponse])
async def my_clues(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await crud_found_clue.get_by_reporter(db, reporter_id=current_user.id)


@router.get("/{clue_id}", response_model=FoundClueResponse)
async def get_clue(
    clue_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    clue = await crud_found_clue.get(db, id=clue_id)
    if not clue:
        raise HTTPException(status_code=404, detail="Clue not found")
    return clue


@router.patch("/{clue_id}/status", response_model=FoundClueResponse)
async def review_clue(
    clue_id: UUID,
    obj_in: FoundClueUpdate,
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    clue = await crud_found_clue.get(db, id=clue_id)
    if not clue:
        raise HTTPException(status_code=404, detail="Clue not found")
    return await crud_found_clue.update_status(db, db_obj=clue, obj_in=obj_in, reviewer_id=admin.id)
