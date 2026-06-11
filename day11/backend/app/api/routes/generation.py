from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.resume import Resume
from app.models.job import JobDescription, CoverLetter, ColdEmail
from app.schemas.schemas import (
    CoverLetterRequest, CoverLetterResponse,
    ColdEmailRequest, ColdEmailResponse,
    LinkedInRequest, LinkedInResponse,
    InterviewRequest, InterviewResponse,
)
from app.services import get_ai_service

ollama = get_ai_service()


async def _fetch_resume_and_jd(resume_id, jd_id, user_id, db):
    r = await db.execute(select(Resume).where(Resume.id == resume_id, Resume.user_id == user_id))
    resume = r.scalar_one_or_none()
    if not resume:
        raise HTTPException(404, "Resume not found")

    j = await db.execute(select(JobDescription).where(JobDescription.id == jd_id, JobDescription.user_id == user_id))
    jd = j.scalar_one_or_none()
    if not jd:
        raise HTTPException(404, "Job description not found")

    return resume, jd


# ── Cover Letter ──────────────────────────────────────────────────────────────
cover_router = APIRouter(prefix="/api/cover-letter", tags=["cover-letter"])


@cover_router.post("/", response_model=CoverLetterResponse, status_code=201)
async def generate_cover_letter(
    data: CoverLetterRequest,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    resume, jd = await _fetch_resume_and_jd(data.resume_id, data.job_description_id, user_id, db)

    content = await ollama.generate_cover_letter(
        resume.parsed_data or {},
        jd.parsed_data or {},
        data.company or jd.company or "",
    )

    letter = CoverLetter(
        id=str(uuid.uuid4()),
        user_id=user_id,
        resume_id=resume.id,
        job_description_id=jd.id,
        content=content,
        company=data.company or jd.company,
    )
    db.add(letter)
    await db.commit()
    await db.refresh(letter)
    return letter


@cover_router.get("/")
async def list_cover_letters(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CoverLetter).where(CoverLetter.user_id == user_id)
        .order_by(CoverLetter.created_at.desc())
    )
    return result.scalars().all()


# ── Cold Email ────────────────────────────────────────────────────────────────
email_router = APIRouter(prefix="/api/cold-email", tags=["cold-email"])


@email_router.post("/", response_model=ColdEmailResponse, status_code=201)
async def generate_cold_email(
    data: ColdEmailRequest,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    resume, jd = await _fetch_resume_and_jd(data.resume_id, data.job_description_id, user_id, db)

    result = await ollama.generate_cold_email(
        resume.parsed_data or {},
        jd.parsed_data or {},
        data.recruiter_email,
        data.company,
    )

    email = ColdEmail(
        id=str(uuid.uuid4()),
        user_id=user_id,
        resume_id=resume.id,
        job_description_id=jd.id,
        recruiter_email=data.recruiter_email,
        company=data.company,
        subject=result["subject"],
        body=result["body"],
    )
    db.add(email)
    await db.commit()
    await db.refresh(email)
    return email


@email_router.get("/")
async def list_cold_emails(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ColdEmail).where(ColdEmail.user_id == user_id)
        .order_by(ColdEmail.created_at.desc())
    )
    return result.scalars().all()


# ── LinkedIn ──────────────────────────────────────────────────────────────────
linkedin_router = APIRouter(prefix="/api/linkedin", tags=["linkedin"])


@linkedin_router.post("/optimize", response_model=LinkedInResponse)
async def optimize_linkedin(
    data: LinkedInRequest,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(select(Resume).where(Resume.id == data.resume_id, Resume.user_id == user_id))
    resume = r.scalar_one_or_none()
    if not resume:
        raise HTTPException(404, "Resume not found")

    parsed = resume.parsed_data or {}
    result = await ollama.optimize_linkedin(parsed)

    # Fallback if AI returns empty
    if not result.get("headline"):
        name = parsed.get("name", "Professional")
        skills = parsed.get("skills", [])
        exp = parsed.get("experience", [{}])
        title = exp[0].get("title", "Professional") if exp else "Professional"
        result = {
            "headline": f"{title} | {', '.join(skills[:3])}" if skills else title,
            "about": f"Experienced {title} with expertise in {', '.join(skills[:5])}. Passionate about delivering high-quality results and driving innovation.",
            "experience_rewrites": [],
        }

    return result


# ── Interview ─────────────────────────────────────────────────────────────────
interview_router = APIRouter(prefix="/api/interview", tags=["interview"])


@interview_router.post("/questions", response_model=InterviewResponse)
async def generate_interview_questions(
    data: InterviewRequest,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    resume, jd = await _fetch_resume_and_jd(data.resume_id, data.job_description_id, user_id, db)

    result = await ollama.generate_interview_questions(
        resume.parsed_data or {},
        jd.parsed_data or {},
    )
    return result
