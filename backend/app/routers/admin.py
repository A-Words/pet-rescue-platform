from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_adoption_application import crud_adoption_application
from app.crud.crud_found_clue import crud_found_clue
from app.crud.crud_lost_pet import crud_lost_pet
from app.crud.crud_adoptable_pet import crud_adoptable_pet
from app.crud.crud_review_record import crud_review_record
from app.crud.crud_visit_reminder import crud_visit_reminder
from app.dependencies import require_admin, get_db
from app.models.lost_pet import LostPet
from app.models.adoptable_pet import AdoptablePet
from app.models.found_clue import FoundClue
from app.models.user import User
from app.schemas.adoption_application import ApplicationReview, AdoptionApplicationResponse
from app.schemas.found_clue import FoundClueResponse
from app.schemas.statistics import DashboardOverview, MonthlyStatistics
from app.schemas.visit_reminder import VisitReminderResponse, VisitReminderUpdate

router = APIRouter()


# === Applications ===

@router.get("/applications", response_model=dict)
async def list_applications(
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    status: str | None = None,
):
    skip = (page - 1) * page_size
    items, total = await crud_adoption_application.get_multi(db, skip=skip, limit=page_size, status=status)
    return {
        "items": [AdoptionApplicationResponse.model_validate(a) for a in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("/applications/{app_id}/review", response_model=AdoptionApplicationResponse)
async def review_application(
    app_id: UUID,
    body: ApplicationReview,
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    app = await crud_adoption_application.get(db, id=app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    if app.status != "pending":
        raise HTTPException(status_code=400, detail="Application already reviewed")

    # Create review record
    await crud_review_record.create(
        db,
        application_id=app_id,
        reviewer_id=admin.id,
        decision=body.decision,
        review_notes=body.review_notes,
    )

    # Update application status (triggers will fire automatically)
    app.status = body.decision
    await db.commit()
    await db.refresh(app)
    return app


# === Statistics ===

@router.get("/statistics", response_model=MonthlyStatistics)
async def get_statistics(
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
):
    result = await db.execute(
        text("SELECT * FROM sp_monthly_statistics(:year, :month)"),
        {"year": year, "month": month},
    )
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=500, detail="Failed to get statistics")
    return MonthlyStatistics(
        total_lost_reports=row.total_lost_reports,
        successful_recoveries=row.successful_recoveries,
        recovery_rate=row.recovery_rate,
        total_adoption_applications=row.total_adoption_applications,
        approved_adoptions=row.approved_adoptions,
        adoption_success_rate=row.adoption_success_rate,
        total_found_clues=row.total_found_clues,
        confirmed_clues=row.confirmed_clues,
    )


@router.get("/statistics/overview", response_model=DashboardOverview)
async def get_dashboard_overview(
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    from app.models.adoption_application import AdoptionApplication
    from app.models.visit_reminder import VisitReminder
    from datetime import date

    active_lost = (await db.execute(
        select(func.count(LostPet.id)).where(LostPet.status == "active")
    )).scalar() or 0

    available_adoptable = (await db.execute(
        select(func.count(AdoptablePet.id)).where(AdoptablePet.adoption_status == "available")
    )).scalar() or 0

    pending_apps = (await db.execute(
        select(func.count(AdoptionApplication.id)).where(AdoptionApplication.status == "pending")
    )).scalar() or 0

    pending_clues = (await db.execute(
        select(func.count(FoundClue.id)).where(FoundClue.status == "pending")
    )).scalar() or 0

    overdue_reminders = await crud_visit_reminder.count_overdue(db)

    return DashboardOverview(
        active_lost_pets=active_lost,
        available_adoptable=available_adoptable,
        pending_applications=pending_apps,
        pending_clues=pending_clues,
        overdue_reminders=overdue_reminders,
    )


# === Visit Reminders ===

@router.get("/visit-reminders", response_model=dict)
async def list_reminders(
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    status: str | None = None,
):
    skip = (page - 1) * page_size
    items, total = await crud_visit_reminder.get_multi(db, skip=skip, limit=page_size, status=status)
    return {
        "items": [VisitReminderResponse.model_validate(r) for r in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.patch("/visit-reminders/{reminder_id}", response_model=VisitReminderResponse)
async def update_reminder(
    reminder_id: UUID,
    obj_in: VisitReminderUpdate,
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    from app.models.visit_reminder import VisitReminder
    result = await db.execute(select(VisitReminder).where(VisitReminder.id == reminder_id))
    reminder = result.scalar_one_or_none()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return await crud_visit_reminder.update(db, db_obj=reminder, obj_in=obj_in)


# === Clues ===

@router.get("/clues", response_model=dict)
async def list_all_clues(
    admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    status: str | None = None,
):
    skip = (page - 1) * page_size
    items, total = await crud_found_clue.get_multi(db, skip=skip, limit=page_size, status=status)
    return {
        "items": [FoundClueResponse.model_validate(c) for c in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }
