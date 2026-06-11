from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ─── Auth ─────────────────────────────────────────────
class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    name: str
    email: str


# ─── Resume ───────────────────────────────────────────
class ParsedResume(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = []
    experience: List[Dict[str, Any]] = []
    education: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    certifications: List[str] = []
    achievements: List[str] = []


class ResumeResponse(BaseModel):
    id: str
    filename: str
    file_path: Optional[str] = None
    raw_text: Optional[str] = None
    parsed_data: Optional[ParsedResume] = None
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── Job Description ──────────────────────────────────
class JobAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=50)
    company: Optional[str] = None
    source_url: Optional[str] = None


class ParsedJob(BaseModel):
    job_title: str = ""
    company: str = ""
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    keywords: List[str] = []
    experience: str = ""
    education: str = ""
    responsibilities: List[str] = []


class JobResponse(BaseModel):
    id: str
    title: Optional[str]
    company: Optional[str]
    parsed_data: Optional[ParsedJob] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ─── ATS ──────────────────────────────────────────────
class ATSScoreRequest(BaseModel):
    resume_id: str
    job_description_id: str


class ATSScoreResponse(BaseModel):
    id: str
    ats_score: float
    keyword_match: float
    skill_match: float
    experience_match: float
    education_match: float
    formatting: float
    readability: float
    missing_keywords: List[str] = []
    missing_skills: List[str] = []
    suggestions: List[str] = []
    optimized_resume: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Cover Letter ─────────────────────────────────────
class CoverLetterRequest(BaseModel):
    resume_id: str
    job_description_id: str
    company: Optional[str] = None


class CoverLetterResponse(BaseModel):
    id: str
    content: str
    company: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Cold Email ───────────────────────────────────────
class ColdEmailRequest(BaseModel):
    resume_id: str
    job_description_id: str
    recruiter_email: str
    company: str


class ColdEmailResponse(BaseModel):
    id: str
    subject: str
    body: str
    recruiter_email: str
    company: str
    created_at: datetime

    class Config:
        from_attributes = True


# ─── LinkedIn ─────────────────────────────────────────
class LinkedInRequest(BaseModel):
    resume_id: str


class LinkedInResponse(BaseModel):
    headline: str
    about: str
    experience_rewrites: List[Dict[str, str]] = []


# ─── Interview ────────────────────────────────────────
class InterviewRequest(BaseModel):
    resume_id: str
    job_description_id: str


class InterviewResponse(BaseModel):
    technical: List[str] = []
    hr: List[str] = []
    behavioral: List[str] = []
