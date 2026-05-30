from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_adoption_application import crud_adoption_application
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.adoption_application import AdoptionApplicationCreate, AdoptionApplicationResponse

router = APIRouter()


@router.post("", response_model=AdoptionApplicationResponse, status_code=status.HTTP_201_CREATED)
async def submit_application(
    obj_in: AdoptionApplicationCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        app = await crud_adoption_application.create(db, obj_in=obj_in, applicant_id=current_user.id)
        return app
    except Exception as e:
        if "duplicate" in str(e).lower() or "unique_violation" in str(e).lower():
            raise HTTPException(status_code=400, detail="您已提交过该宠物的领养申请")
        raise


@router.get("/my", response_model=list[AdoptionApplicationResponse])
async def my_applications(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await crud_adoption_application.get_by_applicant(db, applicant_id=current_user.id)


@router.get("/{app_id}", response_model=AdoptionApplicationResponse)
async def get_application(
    app_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    app = await crud_adoption_application.get(db, id=app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if app.applicant_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return app


@router.patch("/{app_id}/cancel", response_model=AdoptionApplicationResponse)
async def cancel_application(
    app_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    app = await crud_adoption_application.get(db, id=app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if app.applicant_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if app.status != "pending":
        raise HTTPException(status_code=400, detail="Can only cancel pending applications")
    return await crud_adoption_application.cancel(db, db_obj=app)
