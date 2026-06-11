from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.job import JobDescription
from app.schemas.schemas import JobAnalysisRequest, JobResponse
from app.services import get_ai_service

router = APIRouter(prefix="/api/job", tags=["job"])
ollama = get_ai_service()


@router.post("/analyze", status_code=201)
async def analyze_job(
    data: JobAnalysisRequest,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    jd = JobDescription(
        id=str(uuid.uuid4()),
        user_id=user_id,
        raw_text=data.text,
        company=data.company,
        source_url=data.source_url,
    )
    db.add(jd)
    await db.commit()
    await db.refresh(jd)

    background_tasks.add_task(_analyze_jd, jd.id, data.text)

    return {
        "id": jd.id,
        "message": "Job description saved. Analysis in progress...",
    }


async def _analyze_jd(jd_id: str, text: str):
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        try:
            parsed = await ollama.analyze_job(text)
            result = await db.execute(select(JobDescription).where(JobDescription.id == jd_id))
            jd = result.scalar_one_or_none()
            if jd:
                jd.parsed_data = parsed
                jd.title = parsed.get("job_title", "")
                await db.commit()
        except Exception as e:
            from loguru import logger
            logger.error(f"JD analysis failed for {jd_id}: {e}")


@router.get("/", response_model=List[JobResponse])
async def list_jobs(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(JobDescription).where(JobDescription.user_id == user_id)
        .order_by(JobDescription.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{jd_id}")
async def get_job(
    jd_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(JobDescription).where(JobDescription.id == jd_id, JobDescription.user_id == user_id)
    )
    jd = result.scalar_one_or_none()
    if not jd:
        raise HTTPException(404, "Job description not found")
    return jd
