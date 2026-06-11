import json
import re
import httpx
from typing import Any, Dict, Optional
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings


class OpenRouterService:
    """Wrapper around OpenRouter API for all AI tasks using NVIDIA Nemotron."""

    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.timeout = 120  # Reduced timeout for faster responses
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "ATS Resume Optimizer",
        }
        # Connection pool for better performance
        self._client = httpx.AsyncClient(
            timeout=self.timeout,
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5,
                keepalive_expiry=30
            )
        )

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(min=0.5, max=3))
    async def generate(self, model: str, prompt: str, system: str = "") -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.1,
            "top_p": 0.9,
            "max_tokens": 4096,
        }

        try:
            resp = await self._client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=self.headers,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except httpx.TimeoutException:
            logger.warning(f"Timeout for model {model}, retrying...")
            raise
        except Exception as e:
            logger.error(f"API error: {e}")
            raise

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
        system = """Extract resume data as JSON. No markdown, no explanation."""

        prompt = f"""Parse resume to JSON:
{{"name":"","email":"","phone":"","linkedin":"","github":"","summary":"","skills":[],"experience":[{{"title":"","company":"","duration":"","description":""}}],"education":[{{"degree":"","institution":"","year":""}}],"projects":[{{"name":"","description":"","technologies":[]}}],"certifications":[],"achievements":[]}}

Resume:
{resume_text[:3000]}

JSON:"""

        try:
            raw = await self.generate(settings.OPENROUTER_RESUME_PARSE_MODEL, prompt, system)
            return await self.parse_json_response(raw)
        except Exception as e:
            logger.warning(f"AI resume parsing failed, using fallback: {e}")
            return self._fallback_parse_resume(resume_text)

    def _fallback_parse_resume(self, text: str) -> Dict[str, Any]:
        import re
        lines = text.strip().split('\n')
        name = lines[0].strip() if lines else ""
        email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
        phone_match = re.search(r'[\+]?[\d\s\-\(\)]{10,}', text)
        skills = re.findall(r'(?:Skills?|Technologies?|STACK)[:\s]+(.+?)(?:\n|$)', text, re.IGNORECASE)
        return {
            "name": name,
            "email": email_match.group(0) if email_match else "",
            "phone": phone_match.group(0).strip() if phone_match else "",
            "linkedin": "",
            "github": "",
            "summary": "",
            "skills": [s.strip() for s in skills[0].split(',')] if skills else [],
            "experience": [],
            "education": [],
            "projects": [],
            "certifications": [],
            "achievements": [],
        }

    async def analyze_job(self, jd_text: str) -> Dict[str, Any]:
        system = "Extract job requirements as JSON."

        prompt = f"""Analyze job description to JSON:
{{"job_title":"","company":"","required_skills":[],"preferred_skills":[],"keywords":[],"experience":"","education":"","responsibilities":[]}}

Job:
{jd_text[:3000]}

JSON:"""

        try:
            raw = await self.generate(settings.OPENROUTER_ATS_MODEL, prompt, system)
            return await self.parse_json_response(raw)
        except Exception as e:
            logger.warning(f"AI job analysis failed, using fallback: {e}")
            return self._fallback_analyze_job(jd_text)

    def _fallback_analyze_job(self, text: str) -> Dict[str, Any]:
        import re
        lines = text.strip().split('\n')
        title = lines[0].strip() if lines else ""
        company_match = re.search(r'(?:at|Company|Organization)[:\s]+(.+?)(?:\n|$)', text, re.IGNORECASE)
        skills = re.findall(r'(?:Skills?|Requirements?|Qualifications?)[:\s]+(.+?)(?:\n|$)', text, re.IGNORECASE)
        return {
            "job_title": title,
            "company": company_match.group(1).strip() if company_match else "",
            "required_skills": [s.strip() for s in skills[0].split(',')] if skills else [],
            "preferred_skills": [],
            "keywords": [],
            "experience": "",
            "education": "",
            "responsibilities": [],
        }

    async def calculate_ats_score(
        self, resume_text: str, jd_text: str, parsed_resume: Dict, parsed_job: Dict
    ) -> Dict[str, Any]:
        resume_skills = parsed_resume.get("skills", [])
        job_keywords = parsed_job.get("keywords", [])
        job_skills = parsed_job.get("required_skills", []) + parsed_job.get("preferred_skills", [])
        
        matching_skills = set(s.lower() for s in resume_skills) & set(s.lower() for s in job_skills)
        skill_ratio = len(matching_skills) / max(len(job_skills), 1)

        try:
            system = """You are a senior ATS scoring engine used by Fortune 500 recruiters.
Score objectively based on actual content matching. Be generous with scores when the resume genuinely matches the job requirements.
Return ONLY valid JSON."""

            prompt = f"""Score this resume against the job description.

SCORING RULES:
- KEYWORD_MATCH: Count how many job keywords appear in the resume (case-insensitive). Score = (found/total)*100
- SKILL_MATCH: Count matching skills between resume and job requirements. Score = (matched/required)*100. Give partial credit for related skills.
- EXPERIENCE_MATCH: Check if years and seniority level align. Score 80+ if reasonable match.
- EDUCATION_MATCH: Check if degree level meets requirements. Score 90+ if meets or exceeds.
- FORMATTING: Score 85+ for well-structured resumes with clear sections.
- READABILITY: Score 85+ for clear, concise writing.

Resume skills: {resume_skills}
Job keywords: {job_keywords}
Job required skills: {job_skills}
Matching skills found: {list(matching_skills)}
Skill match ratio: {skill_ratio:.0%}

Resume (excerpt):
{resume_text[:3000]}

Job Description (excerpt):
{jd_text[:3000]}

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

            raw = await self.generate(settings.OPENROUTER_ATS_MODEL, prompt, system)
            data = await self.parse_json_response(raw)
        except Exception as e:
            logger.warning(f"AI ATS scoring failed, using rule-based fallback: {e}")
            data = {}

        def safe_float(v, default=70.0):
            try:
                return float(v)
            except (TypeError, ValueError):
                return default

        # If AI returned data, use it; otherwise compute from skill matching
        if data and data.get("ats_score") is not None:
            k = safe_float(data.get("keyword_match"))
            s = safe_float(data.get("skill_match"))
            e = safe_float(data.get("experience_match"))
            ed = safe_float(data.get("education_match"))
            f = safe_float(data.get("formatting"))
            r = safe_float(data.get("readability"))
            missing_kw = data.get("missing_keywords", [])
            missing_sk = data.get("missing_skills", [])
            suggestions = data.get("suggestions", [])
        else:
            # Rule-based fallback scoring
            k = min(skill_ratio * 100, 95)
            s = min(skill_ratio * 100, 95)
            e = 80.0 if skill_ratio > 0.3 else 60.0
            ed = 85.0
            f = 85.0
            r = 85.0
            missing_kw = [kw for kw in job_keywords if kw.lower() not in resume_text.lower()]
            missing_sk = [sk for sk in job_skills if sk.lower() not in [s.lower() for s in resume_skills]]
            suggestions = [f"Consider adding {kw} to your resume" for kw in missing_kw[:5]]

        computed = (k * 0.30 + s * 0.20 + e * 0.20 + ed * 0.10 + f * 0.10 + r * 0.10)

        return {
            "ats_score": round(computed, 1),
            "keyword_match": round(k, 1),
            "skill_match": round(s, 1),
            "experience_match": round(e, 1),
            "education_match": round(ed, 1),
            "formatting": round(f, 1),
            "readability": round(r, 1),
            "missing_keywords": missing_kw,
            "missing_skills": missing_sk,
            "suggestions": suggestions,
        }

    async def calculate_ats_score_and_optimize(
        self, resume_text: str, jd_text: str, parsed_resume: Dict, parsed_job: Dict
    ) -> Dict[str, Any]:
        """Run ATS scoring and resume optimization in parallel for speed."""
        import asyncio

        async def score_task():
            return await self.calculate_ats_score(resume_text, jd_text, parsed_resume, parsed_job)

        async def optimize_task(score_data):
            return await self.optimize_resume(resume_text, jd_text, score_data)

        # Run score first, then optimize (optimize needs score data)
        score_data = await score_task()
        optimized_resume = await optimize_task(score_data)

        return {
            **score_data,
            "optimized_resume": optimized_resume,
        }

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()

    def __del__(self):
        """Cleanup on deletion."""
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.close())
        except Exception:
            pass

    async def optimize_resume(self, resume_text: str, jd_text: str, ats_data: Dict) -> str:
        system = """You are an ATS Resume Optimization Engine trained by recruiters and FAANG resume reviewers.
Your goal is to achieve a 90+ ATS score by strategically optimizing the resume.

RULES:
- NEVER fabricate information, skills, projects, experience, or companies
- ONLY rewrite existing content for clarity, ATS compatibility, and impact
- NATURALLY incorporate missing keywords into existing bullet points and descriptions
- Use strong action verbs and quantified achievements where possible
- Ensure keywords from the job description appear in the resume
- Maintain professional tone while maximizing keyword density
- Output a complete, polished resume with clear section headings"""

        missing_kw = ats_data.get('missing_keywords', [])
        missing_sk = ats_data.get('missing_skills', [])
        suggestions = ats_data.get('suggestions', [])

        prompt = f"""Optimize this resume to achieve a 90+ ATS score against the job description.

CRITICAL OPTIMIZATION TASKS:
1. INCORPORATE these missing keywords naturally: {missing_kw}
2. HIGHLIGHT these skills if present in the original: {missing_sk}
3. APPLY these improvements: {suggestions}
4. Add keywords from the job description that match the candidate's experience
5. Use exact phrases from the job posting where truthful

ORIGINAL RESUME:
{resume_text[:3000]}

JOB DESCRIPTION KEY PHRASES:
{jd_text[:2000]}

Return the complete optimized resume. Preserve all original information while strategically placing keywords for maximum ATS compatibility."""

        try:
            return await self.generate(settings.OPENROUTER_OPTIMIZE_MODEL, prompt, system)
        except Exception as e:
            logger.warning(f"AI resume optimization failed, returning original: {e}")
            return resume_text

    async def generate_cover_letter(self, resume_data: Dict, jd_data: Dict, company: str) -> str:
        system = "Expert cover letter writer. Be specific, compelling, no generic phrases."

        name = resume_data.get('name', 'Candidate')
        skills = resume_data.get('skills', [])[:8]
        title = resume_data.get('experience', [{}])[0].get('title', 'Professional') if resume_data.get('experience') else 'Professional'
        job_title = jd_data.get('job_title', 'the position')
        comp = company or jd_data.get('company', 'the company')
        req_skills = jd_data.get('required_skills', [])[:6]

        prompt = f"""Cover letter for {name} applying to {job_title} at {comp}.

Skills: {', '.join(skills)}
Experience: {title}
Required: {', '.join(req_skills)}

Write 300-400 words. Start "Dear Hiring Manager," end with CTA. No generic phrases."""

        try:
            return await self.generate(settings.OPENROUTER_COVER_LETTER_MODEL, prompt, system)
        except Exception as e:
            logger.warning(f"AI cover letter failed, using fallback: {e}")
            return self._fallback_cover_letter(name, skills, title, job_title, comp, req_skills)

    def _fallback_cover_letter(self, name: str, skills: list, title: str, job_title: str, company: str, req_skills: list) -> str:
        skills_text = ", ".join(skills[:5]) if skills else "my technical skills"
        return f"""Dear Hiring Manager,

I am excited to apply for the {job_title} position at {company}. With my background as a {title} and expertise in {skills_text}, I am confident in my ability to make a meaningful contribution to your team.

Throughout my career, I have developed strong skills in {skills_text} that directly align with your requirements. My experience includes designing and implementing scalable solutions, collaborating with cross-functional teams, and delivering high-quality results under tight deadlines.

I am particularly drawn to {company} because of your commitment to innovation and excellence. I am eager to bring my technical expertise and passion for building great software to your organization.

I would welcome the opportunity to discuss how my skills and experience align with your needs. Thank you for considering my application.

Best regards,
{name}"""

    async def generate_cold_email(self, resume_data: Dict, jd_data: Dict, recruiter_email: str, company: str) -> Dict[str, str]:
        system = "Expert recruiter outreach. Write concise, compelling cold emails."

        name = resume_data.get('name', 'Candidate')
        skills = resume_data.get('skills', [])[:5]
        title = resume_data.get('experience', [{}])[0].get('title', '') if resume_data.get('experience') else ''
        job_title = jd_data.get('job_title', 'the position')

        prompt = f"""Cold email to recruiter for {name}.

Skills: {', '.join(skills)}
Role: {title}
Job: {job_title} at {company}

JSON: {{"subject": "email subject", "body": "150-200 word email"}}

Personal, specific, professional. Clear CTA. JSON only."""

        try:
            raw = await self.generate(settings.OPENROUTER_COLD_EMAIL_MODEL, prompt, system)
            data = await self.parse_json_response(raw)
            if data.get("subject"):
                return {
                    "subject": data.get("subject", f"Exploring opportunities at {company}"),
                    "body": data.get("body", raw),
                }
        except Exception as e:
            logger.warning(f"AI cold email failed, using fallback: {e}")

        return self._fallback_cold_email(name, skills, title, job_title, company)

    def _fallback_cold_email(self, name: str, skills: list, title: str, job_title: str, company: str) -> Dict[str, str]:
        skills_text = ", ".join(skills[:3]) if skills else "my relevant skills"
        return {
            "subject": f"Interested in {job_title} opportunity at {company}",
            "body": f"""Hi,

I'm {name}, a {title} with experience in {skills_text}. I came across the {job_title} role at {company} and wanted to reach out directly.

I believe my background makes me a strong fit for this position. I'd love the opportunity to discuss how I can contribute to your team.

Would you be available for a brief call this week?

Best,
{name}""",
        }

    async def optimize_linkedin(self, resume_data: Dict) -> Dict[str, Any]:
        system = "You are a LinkedIn profile optimization expert."

        name = resume_data.get('name', '')
        title = resume_data.get('experience', [{}])[0].get('title', '') if resume_data.get('experience') else ''
        skills = resume_data.get('skills', [])[:15]

        prompt = f"""Optimize this professional's LinkedIn profile.

Name: {name}
Current title: {title}
Skills: {', '.join(skills)}
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

        try:
            raw = await self.generate(settings.OPENROUTER_OPTIMIZE_MODEL, prompt, system)
            return await self.parse_json_response(raw)
        except Exception as e:
            logger.warning(f"AI LinkedIn optimization failed, using fallback: {e}")
            return self._fallback_linkedin(name, title, skills)

    def _fallback_linkedin(self, name: str, title: str, skills: list) -> Dict[str, Any]:
        skills_text = ", ".join(skills[:5]) if skills else "various technologies"
        return {
            "headline": f"{title} | {skills_text}" if title else skills_text,
            "about": f"Experienced {title if title else 'professional'} with expertise in {skills_text}. Passionate about delivering high-quality results, building scalable solutions, and driving innovation. Strong background in collaborative team environments with a focus on continuous learning and growth.",
            "experience_rewrites": [],
        }

    async def generate_interview_questions(self, resume_data: Dict, jd_data: Dict) -> Dict[str, Any]:
        system = "You are a senior technical recruiter and interviewer."

        role = jd_data.get('job_title', 'the position')
        req_skills = jd_data.get('required_skills', [])[:8]
        cand_skills = resume_data.get('skills', [])[:10]

        prompt = f"""Generate interview questions for this candidate and role.

ROLE: {role}
REQUIRED SKILLS: {', '.join(req_skills)}
CANDIDATE SKILLS: {', '.join(cand_skills)}

Return JSON:
{{
  "technical": ["5 technical questions based on the role and skills"],
  "hr": ["4 HR/culture fit questions"],
  "behavioral": ["4 behavioral STAR questions"]
}}

Make questions specific to the role and candidate. Return ONLY JSON."""

        try:
            raw = await self.generate(settings.OPENROUTER_ATS_MODEL, prompt, system)
            data = await self.parse_json_response(raw)
            if data.get("technical"):
                return {
                    "technical": data.get("technical", []),
                    "hr": data.get("hr", []),
                    "behavioral": data.get("behavioral", []),
                }
        except Exception as e:
            logger.warning(f"AI interview generation failed, using fallback: {e}")

        # Fallback: generate reasonable questions from available data
        return self._fallback_interview_questions(role, req_skills, cand_skills)

    def _fallback_interview_questions(self, role: str, req_skills: list, cand_skills: list) -> Dict[str, Any]:
        skills_str = ", ".join(req_skills[:5]) if req_skills else "the required technologies"
        cand_str = ", ".join(cand_skills[:5]) if cand_skills else "your technical background"
        
        technical = [
            f"Can you walk us through a complex project where you used {skills_str}?",
            f"How do you approach system design for a {role} role?",
            f"Describe your experience with {skills_str}. What challenges did you face?",
            f"How do you ensure code quality and maintainability in your projects?",
            f"Tell us about a time you had to learn a new technology quickly.",
        ]
        hr = [
            "Why are you interested in this position?",
            "How do you handle tight deadlines and competing priorities?",
            "Describe your ideal work environment.",
            "Where do you see yourself in 5 years?",
        ]
        behavioral = [
            "Tell me about a time you had a conflict with a teammate. How did you resolve it?",
            "Describe a project where you had to make a difficult technical decision.",
            "Give an example of when you went above and beyond for a project.",
            "Tell us about a time you failed. What did you learn from it?",
        ]
        return {"technical": technical, "hr": hr, "behavioral": behavioral}
