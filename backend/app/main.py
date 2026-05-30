import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.dependencies import get_current_user
from app.models.user import User
from app.routers import admin, adoption_applications, adoptable_pets, auth, found_clues, lost_pets
from app.services.file_service import save_upload_file


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    yield


app = FastAPI(title="Lost Pet & Adoption Rescue System", version="1.0.0", lifespan=lifespan, redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(lost_pets.router, prefix="/api/lost-pets", tags=["Lost Pets"])
app.include_router(found_clues.router, prefix="/api/found-clues", tags=["Found Clues"])
app.include_router(adoptable_pets.router, prefix="/api/adoptable-pets", tags=["Adoptable Pets"])
app.include_router(adoption_applications.router, prefix="/api/adoption-applications", tags=["Adoption Applications"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.post("/api/upload/image")
async def upload_image(
    file: UploadFile,
    current_user: Annotated[User, Depends(get_current_user)],
):
    url = await save_upload_file(file)
    return {"url": url}


@app.get("/api/health")
async def health():
    return {"status": "ok"}
