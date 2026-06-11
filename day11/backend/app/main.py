import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger
from app.core.config import settings
from app.core.database import create_tables
from app.api.routes.resume import router as resume_router
from app.api.routes.job import router as job_router
from app.api.routes.ats import router as ats_router
from app.api.routes.generation import (
    cover_router, email_router, linkedin_router, interview_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting ATS Resume Optimizer API...")
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.CHROMA_PATH, exist_ok=True)
    await create_tables()
    logger.info("Database tables ready")
    if settings.USE_OPENROUTER:
        logger.info(f"AI Service: OpenRouter (model: {settings.OPENROUTER_ATS_MODEL})")
    else:
        logger.info(f"AI Service: Ollama ({settings.OLLAMA_BASE_URL})")
    yield
    # Cleanup AI service connections
    from app.services import get_ai_service
    ai_service = get_ai_service()
    if hasattr(ai_service, 'close'):
        await ai_service.close()
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="ATS Resume Optimizer & AI Job Application Assistant",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(resume_router)
app.include_router(job_router)
app.include_router(ats_router)
app.include_router(cover_router)
app.include_router(email_router)
app.include_router(linkedin_router)
app.include_router(interview_router)


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
