from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.resume import Resume
from app.models.job import JobDescription, ATSReport
from app.schemas.schemas import ATSScoreRequest, ATSScoreResponse
from app.services import get_ai_service

router = APIRouter(prefix="/api/ats", tags=["ats"])
ollama = get_ai_service()


@router.post("/score", response_model=ATSScoreResponse)
async def calculate_ats_score(
    data: ATSScoreRequest,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(
        select(Resume).where(Resume.id == data.resume_id, Resume.user_id == user_id)
    )
    resume = r.scalar_one_or_none()
    if not resume:
        raise HTTPException(404, "Resume not found")

    j = await db.execute(
        select(JobDescription).where(
            JobDescription.id == data.job_description_id,
            JobDescription.user_id == user_id,
        )
    )
    jd = j.scalar_one_or_none()
    if not jd:
        raise HTTPException(404, "Job description not found")

    resume_text = resume.raw_text or ""
    jd_text = jd.raw_text or ""
    parsed_resume = resume.parsed_data or {}
    parsed_job = jd.parsed_data or {}

    result = await ollama.calculate_ats_score_and_optimize(
        resume_text, jd_text, parsed_resume, parsed_job
    )
    score_data = result
    optimized = result.get("optimized_resume", "")

    report = ATSReport(
        id=str(uuid.uuid4()),
        user_id=user_id,
        resume_id=resume.id,
        job_description_id=jd.id,
        ats_score=score_data["ats_score"],
        keyword_match=score_data["keyword_match"],
        skill_match=score_data["skill_match"],
        experience_match=score_data["experience_match"],
        education_match=score_data["education_match"],
        formatting=score_data["formatting"],
        readability=score_data["readability"],
        missing_keywords=score_data["missing_keywords"],
        missing_skills=score_data["missing_skills"],
        suggestions=score_data["suggestions"],
        optimized_resume=optimized,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)

    return report


@router.get("/reports")
async def list_reports(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ATSReport).where(ATSReport.user_id == user_id)
        .order_by(ATSReport.created_at.desc())
    )
    return result.scalars().all()


@router.get("/reports/{report_id}")
async def get_report(
    report_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ATSReport).where(ATSReport.id == report_id, ATSReport.user_id == user_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(404, "Report not found")
    return report


@router.get("/reports/{report_id}/download")
async def download_optimized_resume(
    report_id: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ATSReport).where(ATSReport.id == report_id, ATSReport.user_id == user_id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(404, "Report not found")
    
    if not report.optimized_resume:
        raise HTTPException(400, "No optimized resume available for this report")
    
    filename = f"optimized_resume_{report_id[:8]}.txt"
    return PlainTextResponse(
        content=report.optimized_resume,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )
