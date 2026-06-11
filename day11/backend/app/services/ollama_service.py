import json
import re
import httpx
import hashlib
from typing import Any, Dict, Optional
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings


class OllamaService:
    """Wrapper around local Ollama API for all AI tasks."""

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.timeout = 300
        self._cache: Dict[str, Dict[str, Any]] = {}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def generate(self, model: str, prompt: str, system: str = "") -> str:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "num_predict": 4096,
            },
        }
        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(f"{self.base_url}/api/generate", json=payload)
            resp.raise_for_status()
            return resp.json().get("response", "")

    async def parse_json_response(self, raw: str) -> Dict[str, Any]:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        cleaned = re.sub(r"```(?:json)?\s*", "", raw).strip().rstrip("```").strip()
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        logger.warning(f"Could not parse JSON from: {raw[:200]}")
        return {}

    async def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        system = """You are an expert resume parser. Extract all information from the resume and return ONLY valid JSON.
No explanation, no markdown fences, just pure JSON."""

        prompt = f"""Parse this resume and return a JSON object with these exact keys:
{{
  "name": "",
  "email": "",
  "phone": "",
  "linkedin": "",
  "github": "",
  "summary": "",
  "skills": [],
  "experience": [
    {{"title": "", "company": "", "duration": "", "description": ""}}
  ],
  "education": [
    {{"degree": "", "institution": "", "year": ""}}
  ],
  "projects": [
    {{"name": "", "description": "", "technologies": []}}
  ],
  "certifications": [],
  "achievements": []
}}

RESUME TEXT:
{resume_text[:4000]}

Return ONLY the JSON object."""

        raw = await self.generate(settings.OLLAMA_RESUME_PARSE_MODEL, prompt, system)
        return await self.parse_json_response(raw)

    async def analyze_job(self, jd_text: str) -> Dict[str, Any]:
        system = "You are an expert job description analyst. Return ONLY valid JSON, no extra text."

        prompt = f"""Analyze this job description and return JSON:
{{
  "job_title": "",
  "company": "",
  "required_skills": [],
  "preferred_skills": [],
  "keywords": [],
  "experience": "",
  "education": "",
  "responsibilities": []
}}

JOB DESCRIPTION:
{jd_text[:4000]}

Return ONLY the JSON object."""

        raw = await self.generate(settings.OLLAMA_ATS_MODEL, prompt, system)
        return await self.parse_json_response(raw)

    async def calculate_ats_score(
        self, resume_text: str, jd_text: str, parsed_resume: Dict, parsed_job: Dict
    ) -> Dict[str, Any]:
        system = """You are a senior ATS scoring engine used by Fortune 500 recruiters.
Score objectively based on actual content matching. Return ONLY valid JSON."""

        resume_skills = parsed_resume.get("skills", [])
        job_keywords = parsed_job.get("keywords", [])
        job_skills = parsed_job.get("required_skills", []) + parsed_job.get("preferred_skills", [])

        prompt = f"""Score this resume against the job description using this formula:
ATS_SCORE = (KEYWORD×0.30) + (SKILL×0.20) + (EXPERIENCE×0.20) + (EDUCATION×0.10) + (FORMATTING×0.10) + (READABILITY×0.10)

Resume skills: {resume_skills}
Job keywords: {job_keywords}
Job required skills: {job_skills}

Resume (excerpt):
{resume_text[:2000]}

Job Description (excerpt):
{jd_text[:2000]}

Return JSON:
{{
  "ats_score": 0.0,
  "keyword_match": 0.0,
  "skill_match": 0.0,
  "experience_match": 0.0,
  "education_match": 0.0,
  "formatting": 0.0,
  "readability": 0.0,
  "missing_keywords": [],
  "missing_skills": [],
  "suggestions": []
}}

All scores 0-100. Return ONLY JSON."""

        raw = await self.generate(settings.OLLAMA_ATS_MODEL, prompt, system)
        data = await self.parse_json_response(raw)

        def safe_float(v, default=70.0):
            try:
                return float(v)
            except (TypeError, ValueError):
                return default

        k = safe_float(data.get("keyword_match"))
        s = safe_float(data.get("skill_match"))
        e = safe_float(data.get("experience_match"))
        ed = safe_float(data.get("education_match"))
        f = safe_float(data.get("formatting"))
        r = safe_float(data.get("readability"))

        computed = (k * 0.30 + s * 0.20 + e * 0.20 + ed * 0.10 + f * 0.10 + r * 0.10)

        return {
            "ats_score": round(computed, 1),
            "keyword_match": round(k, 1),
            "skill_match": round(s, 1),
            "experience_match": round(e, 1),
            "education_match": round(ed, 1),
            "formatting": round(f, 1),
            "readability": round(r, 1),
            "missing_keywords": data.get("missing_keywords", []),
            "missing_skills": data.get("missing_skills", []),
            "suggestions": data.get("suggestions", []),
        }

    def _cache_key(self, resume_text: str, jd_text: str) -> str:
        combined = f"{resume_text[:1000]}|{jd_text[:1000]}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    async def calculate_ats_score_and_optimize(
        self, resume_text: str, jd_text: str, parsed_resume: Dict, parsed_job: Dict
    ) -> Dict[str, Any]:
        """Run ATS scoring and resume optimization in parallel for speed with caching."""
        cache_key = self._cache_key(resume_text, jd_text)
        
        if cache_key in self._cache:
            logger.info("Returning cached ATS analysis result")
            return self._cache[cache_key]

        async def score_task():
            return await self.calculate_ats_score(resume_text, jd_text, parsed_resume, parsed_job)

        async def optimize_task(score_data):
            return await self.optimize_resume(resume_text, jd_text, score_data)

        score_data = await score_task()
        optimized_resume = await optimize_task(score_data)

        result = {
            **score_data,
            "optimized_resume": optimized_resume,
        }
        
        self._cache[cache_key] = result
        return result

    async def optimize_resume(self, resume_text: str, jd_text: str, ats_data: Dict) -> str:
        system = """You are an ATS Resume Optimization Engine trained by recruiters and FAANG resume reviewers.
RULES:
- NEVER fabricate information, skills, projects, experience, or companies
- ONLY rewrite existing content for clarity, ATS compatibility, and impact
- Improve wording, structure, and keyword placement
- Output a complete, polished resume"""

        prompt = f"""Optimize this resume for the job description below.

Missing keywords to naturally incorporate: {ats_data.get('missing_keywords', [])}
Missing skills to highlight if present: {ats_data.get('missing_skills', [])}
Suggestions: {ats_data.get('suggestions', [])}

ORIGINAL RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{jd_text[:2000]}

Return the complete optimized resume text. Do NOT invent any information."""

        return await self.generate(settings.OLLAMA_FAST_MODEL, prompt, system)

    async def generate_cover_letter(self, resume_data: Dict, jd_data: Dict, company: str) -> str:
        system = "You are an expert cover letter writer. Write compelling, personalized cover letters."

        prompt = f"""Write a professional cover letter (300-400 words) for this candidate.

CANDIDATE:
Name: {resume_data.get('name', 'Candidate')}
Skills: {', '.join(resume_data.get('skills', [])[:10])}
Experience: {resume_data.get('experience', [{}])[0].get('title', 'Professional') if resume_data.get('experience') else 'Professional'}

JOB:
Title: {jd_data.get('job_title', 'the position')}
Company: {company or jd_data.get('company', 'the company')}
Required Skills: {', '.join(jd_data.get('required_skills', [])[:8])}

Write a professional, personalized cover letter. Start with "Dear Hiring Manager," and end with a strong CTA.
Do NOT use generic phrases like "I am writing to express my interest". Be specific and compelling."""

        return await self.generate(settings.OLLAMA_COVER_LETTER_MODEL, prompt, system)

    async def generate_cold_email(self, resume_data: Dict, jd_data: Dict, recruiter_email: str, company: str) -> Dict[str, str]:
        system = "You are an expert recruiter outreach specialist. Write concise, compelling cold emails that get responses."

        prompt = f"""Write a cold email to a recruiter (150-200 words total).

CANDIDATE: {resume_data.get('name', 'Candidate')}
TOP SKILLS: {', '.join(resume_data.get('skills', [])[:5])}
EXPERIENCE: {resume_data.get('experience', [{}])[0].get('title', '') if resume_data.get('experience') else ''}

JOB: {jd_data.get('job_title', 'the position')} at {company}
RECRUITER: {recruiter_email}

Return JSON:
{{
  "subject": "compelling email subject line",
  "body": "full email body 150-200 words"
}}

Make it personal, specific, and professional. End with a clear CTA.
Return ONLY JSON."""

        raw = await self.generate(settings.OLLAMA_COLD_EMAIL_MODEL, prompt, system)
        data = await self.parse_json_response(raw)
        return {
            "subject": data.get("subject", "Exploring opportunities at " + company),
            "body": data.get("body", raw),
        }

    async def optimize_linkedin(self, resume_data: Dict) -> Dict[str, Any]:
        system = "You are a LinkedIn profile optimization expert."

        prompt = f"""Optimize this professional's LinkedIn profile.

Name: {resume_data.get('name', '')}
Current title: {resume_data.get('experience', [{}])[0].get('title', '') if resume_data.get('experience') else ''}
Skills: {', '.join(resume_data.get('skills', [])[:15])}
Experience: {json.dumps(resume_data.get('experience', [])[:3])}

Return JSON:
{{
  "headline": "optimized LinkedIn headline (120 chars max)",
  "about": "compelling about section 200-300 words",
  "experience_rewrites": [
    {{"original": "", "optimized": ""}}
  ]
}}

Return ONLY JSON."""

        raw = await self.generate(settings.OLLAMA_OPTIMIZE_MODEL, prompt, system)
        return await self.parse_json_response(raw)

    async def generate_interview_questions(self, resume_data: Dict, jd_data: Dict) -> Dict[str, Any]:
        system = "You are a senior technical recruiter and interviewer."

        prompt = f"""Generate interview questions for this candidate and role.

ROLE: {jd_data.get('job_title', 'the position')}
REQUIRED SKILLS: {', '.join(jd_data.get('required_skills', [])[:8])}
CANDIDATE SKILLS: {', '.join(resume_data.get('skills', [])[:10])}

Return JSON:
{{
  "technical": ["5 technical questions based on the role and skills"],
  "hr": ["4 HR/culture fit questions"],
  "behavioral": ["4 behavioral STAR questions"]
}}

Make questions specific to the role and candidate. Return ONLY JSON."""

        raw = await self.generate(settings.OLLAMA_ATS_MODEL, prompt, system)
        data = await self.parse_json_response(raw)
        return {
            "technical": data.get("technical", []),
            "hr": data.get("hr", []),
            "behavioral": data.get("behavioral", []),
        }
