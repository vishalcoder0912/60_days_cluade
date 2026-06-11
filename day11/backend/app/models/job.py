from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String)
    company = Column(String)
    raw_text = Column(Text, nullable=False)
    parsed_data = Column(JSON)
    source_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="job_descriptions")
    ats_reports = relationship("ATSReport", back_populates="job_description")
    cover_letters = relationship("CoverLetter", back_populates="job_description")
    cold_emails = relationship("ColdEmail", back_populates="job_description")


class ATSReport(Base):
    __tablename__ = "ats_reports"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    resume_id = Column(String, ForeignKey("resumes.id"), nullable=False)
    job_description_id = Column(String, ForeignKey("job_descriptions.id"), nullable=False)

    ats_score = Column(Float, default=0.0)
    keyword_match = Column(Float, default=0.0)
    skill_match = Column(Float, default=0.0)
    experience_match = Column(Float, default=0.0)
    education_match = Column(Float, default=0.0)
    formatting = Column(Float, default=0.0)
    readability = Column(Float, default=0.0)

    missing_keywords = Column(JSON)
    missing_skills = Column(JSON)
    suggestions = Column(JSON)
    optimized_resume = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="ats_reports")
    resume = relationship("Resume", back_populates="ats_reports")
    job_description = relationship("JobDescription", back_populates="ats_reports")


class CoverLetter(Base):
    __tablename__ = "cover_letters"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    resume_id = Column(String, ForeignKey("resumes.id"), nullable=False)
    job_description_id = Column(String, ForeignKey("job_descriptions.id"), nullable=False)
    content = Column(Text, nullable=False)
    company = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="cover_letters")
    resume = relationship("Resume", back_populates="cover_letters")
    job_description = relationship("JobDescription", back_populates="cover_letters")


class ColdEmail(Base):
    __tablename__ = "cold_emails"

    id = Column(String, primary_key=True, default=gen_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    resume_id = Column(String, ForeignKey("resumes.id"), nullable=False)
    job_description_id = Column(String, ForeignKey("job_descriptions.id"), nullable=False)
    recruiter_email = Column(String)
    company = Column(String)
    subject = Column(String)
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="cold_emails")
    resume = relationship("Resume", back_populates="cold_emails")
    job_description = relationship("JobDescription", back_populates="cold_emails")
