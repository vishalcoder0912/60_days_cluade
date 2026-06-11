from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.resume import Resume
from app.schemas.schemas import ResumeResponse
from app.services.file_service import save_upload, extract_text
from app.services import get_ai_service
from app.services.embedding_service import embedding_service

router = APIRouter(prefix="/api/resume", tags=["resume"])
ollama = get_ai_service()


@router.post("/upload", status_code=201)
async def upload_resume(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    file_path, filename = await save_upload(file, user_id)
    raw_text = extract_text(file_path)

    resume = Resume(
        id=str(uuid.uuid4()),
        user_id=user_id,
        filename=filename,
        file_path=file_path,
        raw_text=raw_text,
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)

    background_tasks.add_task(_parse_and_embed, resume.id, raw_text, user_id)

    return {
        "id": resume.id,
        "filename": filename,
        "message": "Resume uploaded. Parsing in progress...",
    }


async def _parse_and_embed(resume_id: str, raw_text: str, user_id: str):
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        try:
            parsed = await ollama.parse_resume(raw_text)
            embedding_id = await embedding_service.store_resume(
                resume_id, user_id, raw_text,
                {"name": parsed.get("name", ""), "skills": str(parsed.get("skills", [])[:5])}
            )
            result = await db.execute(select(Resume).where(Resume.id == resume_id))
            resume = result.scalar_one_or_none()
            if resume:
                resume.parsed_data = parsed
                resume.embedding_id = embedding_id
                await db.commit()
        except Exception as e:
            from loguru import logger
            logger.error(f"Background parse failed for {resume_id}: {e}")


@router.get("/", response_model=List[ResumeResponse])
async def list_resumes(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Resume).where(Resume.user_id == user_id, Resume.is_active == True)
        .order_by(Resume.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{resume_id}")
async def get_resume(
    resume_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == user_id)
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(404, "Resume not found")
    return resume


@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Resume).where(Resume.id == resume_id, Resume.user_id == user_id)
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(404, "Resume not found")
    resume.is_active = False
    await db.commit()
    return {"message": "Resume deleted"}
