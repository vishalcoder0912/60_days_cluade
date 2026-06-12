import "dotenv/config";
import express from "express";
import multer from "multer";
import path from "path";
import { fileURLToPath } from "url";
import { Firecrawl } from "firecrawl";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const upload = multer({ storage: multer.memoryStorage() });

const app = express();
app.use(express.json({ limit: "50mb" }));

// ─── AI Gateway ───────────────────────────────────────────────
const OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions";

function getAiKey(): string {
  const key = process.env.OPENROUTER_API_KEY;
  if (!key) throw new Error("OPENROUTER_API_KEY is not configured");
  return key;
}

function getFirecrawlKey(): string {
  const key = process.env.FIRECRAWL_API_KEY;
  if (!key) throw new Error("FIRECRAWL_API_KEY is not configured");
  return key;
}

type ContentBlock =
  | { type: "text"; text: string }
  | { type: "file"; file: { filename: string; file_data: string } }
  | { type: "image_url"; image_url: { url: string } };

type ChatMessage = {
  role: "system" | "user" | "assistant";
  content: string | ContentBlock[];
};

async function generateText(opts: {
  system: string;
  user: string | ContentBlock[];
  temperature?: number;
  jsonMode?: boolean;
}): Promise<string> {
  const body: Record<string, any> = {
    model: process.env.AI_MODEL || "meta-llama/llama-3.1-8b-instruct",
    messages: [
      { role: "system", content: opts.system },
      { role: "user", content: opts.user },
    ],
    temperature: opts.temperature ?? 0.6,
  };
  if (opts.jsonMode) {
    body.response_format = { type: "json_object" };
  }
  const res = await fetch(OPENROUTER_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getAiKey()}`,
      "HTTP-Referer": "https://careerforge-ai.vercel.app",
      "X-Title": "CareerForge AI",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    if (res.status === 429) throw new Error("RATE_LIMIT: AI is busy right now. Please retry in a moment.");
    throw new Error(`AI error ${res.status}: ${body.slice(0, 500)}`);
  }
  const data = (await res.json()) as { choices?: { message?: { content?: string } }[] };
  return data.choices?.[0]?.message?.content ?? "";
}

async function generateJSON<T>(opts: {
  system: string;
  user: string | ContentBlock[];
  temperature?: number;
}): Promise<T> {
  const raw = await generateText({
    system: opts.system + "\n\nYou MUST respond with a single valid JSON object only. No markdown, no code fences, no commentary.",
    user: opts.user,
    temperature: opts.temperature,
    jsonMode: true,
  });
  return parseJSON<T>(raw);
}

function parseJSON<T>(raw: string): T {
  let text = raw.trim();
  if (text.startsWith("```")) {
    text = text.replace(/^```(?:json)?\s*/i, "").replace(/```\s*$/, "").trim();
  }
  try {
    return JSON.parse(text) as T;
  } catch {
    const start = text.indexOf("{");
    const end = text.lastIndexOf("}");
    if (start !== -1 && end !== -1) {
      return JSON.parse(text.slice(start, end + 1)) as T;
    }
    throw new Error("AI returned malformed JSON.");
  }
}

// ─── Firecrawl Search ─────────────────────────────────────────
let firecrawlClient: Firecrawl | null = null;
function getFirecrawl(): Firecrawl {
  if (!firecrawlClient) {
    firecrawlClient = new Firecrawl({ apiKey: getFirecrawlKey() });
  }
  return firecrawlClient;
}

async function webSearch(query: string, limit = 6) {
  try {
    const data = await getFirecrawl().search(query, { limit });
    return data.web ?? [];
  } catch {
    return [];
  }
}

async function researchDigest(
  queries: string[],
  perQuery = 5,
): Promise<{ digest: string; sources: { title: string; url: string }[] }> {
  const results = await Promise.all(queries.map((q) => webSearch(q, perQuery)));
  const sources: { title: string; url: string }[] = [];
  const seen = new Set<string>();
  const chunks: string[] = [];
  queries.forEach((q, i) => {
    const items = results[i] ?? [];
    if (!items.length) return;
    chunks.push(`### Search: ${q}`);
    for (const item of items) {
      const url = item.url ?? "";
      const title = item.title ?? url;
      const desc = (item.description ?? "").slice(0, 400);
      chunks.push(`- ${title}\n  ${url}\n  ${desc}`);
      if (url && !seen.has(url)) {
        seen.add(url);
        sources.push({ title, url });
      }
    }
  });
  return { digest: chunks.join("\n"), sources: sources.slice(0, 24) };
}

// ─── Resume Parsing Helpers ───────────────────────────────────
async function extractTextFromFile(
  name: string,
  mime: string,
  dataBase64: string,
): Promise<string> {
  const ext = name.split(".").pop()?.toLowerCase();
  const buf = Buffer.from(dataBase64, "base64");

  if (ext === "txt") return buf.toString("utf-8");
  if (ext === "pdf") {
    try {
      const pdfParse = (await import("pdf-parse")).default;
      const data = await pdfParse(buf);
      return data.text;
    } catch {
      return "(PDF text extraction failed — please paste resume text instead)";
    }
  }
  if (ext === "docx" || ext === "doc") {
    try {
      const mammoth = await import("mammoth");
      const result = await mammoth.extractRawText({ buffer: buf });
      return result.value;
    } catch {
      return "(DOCX text extraction failed — please paste resume text instead)";
    }
  }
  return buf.toString("utf-8");
}

// ─── API Routes ───────────────────────────────────────────────

app.post("/api/analyze-resume", async (req, res) => {
  try {
    const { resumeText, resumeFile, role, company, jobDescription, experience, location } = req.body;
    let text = resumeText || "";
    if (resumeFile) {
      text = await extractTextFromFile(resumeFile.name, resumeFile.mime, resumeFile.dataBase64);
    }
    if (!text || text.length < 20) {
      return res.status(400).json({ error: "Could not extract resume text. Please paste your resume directly." });
    }

    const context = [
      `Target role: ${role}`,
      `Target company: ${company}`,
      location ? `Preferred location: ${location}` : "",
      `Experience level: ${experience}`,
      jobDescription ? `Job description:\n${jobDescription}` : "",
    ].filter(Boolean).join("\n");

    const instruction = `Analyze this resume against the target job. Be specific and honest.\n\n${context}\n\nRESUME:\n${text}`;

    const result = await generateJSON({
      system: `You are a senior technical recruiter and ATS optimization expert. You evaluate resumes rigorously.
STRICT JSON SCHEMA — use ONLY these exact keys:
{
  "resumeSummary": string,
  "candidateName": string,
  "atsScore": integer 0-100,
  "resumeHealth": integer 0-100,
  "skills": [string],
  "education": [string],
  "certifications": [string],
  "projects": [{"name": string, "description": string}],
  "workExperience": [{"title": string, "org": string, "highlights": [string]}],
  "keywords": [string],
  "missingKeywords": [string],
  "missingSkills": [string],
  "strengths": [string],
  "weaknesses": [string],
  "suggestions": [string],
  "keywordMatch": [{"keyword": string, "present": boolean}]
}`,
      user: instruction,
      temperature: 0.3,
    });

    res.json(result);
  } catch (err: any) {
    console.error("analyze-resume error:", err);
    res.status(500).json({ error: err.message || "Failed to analyze resume" });
  }
});

app.post("/api/research", async (req, res) => {
  try {
    const { role, company, location } = req.body;

    const { digest, sources } = await researchDigest([
      `${company} company overview mission values`,
      `${company} recent news funding product launch ${new Date().getFullYear()}`,
      `${company} leadership team executives`,
      `${company} tech stack engineering`,
      `${company} work culture glassdoor reviews`,
      `${role} ${company} interview questions experience`,
      `${role} required skills tools responsibilities salary`,
      `${company} competitors`,
    ]);

    const user = `Using the web research below, produce intelligence reports for a ${role} candidate targeting ${company}${location ? " in " + location : ""}.
If the research is sparse, use well-known public knowledge but stay factual.
WEB RESEARCH:
${digest || "(no live results returned)"}`;

    const result = await generateJSON({
      system: `You are a market intelligence analyst specializing in company and job-role research for job seekers.
STRICT JSON SCHEMA — use ONLY these exact keys:
{
  "company": {
    "overview": string, "mission": string, "values": [string],
    "recentNews": [string], "productLaunches": [string], "funding": string,
    "leadership": [{"name": string, "role": string}], "hiringTrends": string,
    "techStack": [string], "culture": string, "interviewExperiences": [string],
    "competitors": [string]
  },
  "role": {
    "requiredSkills": [string], "frequentSkills": [string], "tools": [string],
    "technologies": [string], "certifications": [string], "responsibilities": [string],
    "salaryInsights": string, "careerGrowth": [string]
  }
}`,
      user,
      temperature: 0.4,
    });

    res.json({ ...result, sources });
  } catch (err: any) {
    console.error("research error:", err);
    res.status(500).json({ error: err.message || "Failed to run research" });
  }
});

app.post("/api/build-strategy", async (req, res) => {
  try {
    const { role, company, jobDescription, experience, location, resumeSummary, resumeSkills, roleSkills } = req.body;
    const context = [
      `Target role: ${role}`,
      `Target company: ${company}`,
      location ? `Preferred location: ${location}` : "",
      `Experience level: ${experience}`,
      jobDescription ? `Job description:\n${jobDescription}` : "",
    ].filter(Boolean).join("\n");

    const user = `Compare the candidate's skills to the target role's skills and build a learning roadmap.
${context}
Candidate summary: ${resumeSummary}
Candidate skills: ${(resumeSkills || []).join(", ")}
Target role skills: ${(roleSkills || []).join(", ")}`;

    const result = await generateJSON({
      system: `You are a career coach who builds precise, motivating upskilling plans.
STRICT JSON SCHEMA — use ONLY these exact keys:
{
  "matchingSkills": [string],
  "missingSkills": [string],
  "matchPercent": integer 0-100,
  "plan30": [string],
  "plan60": [string],
  "plan90": [string],
  "learning": [{"skill": string, "why": string, "course": string, "youtube": string, "documentation": string, "practice": string, "projectIdea": string}]
}`,
      user,
      temperature: 0.5,
    });

    res.json(result);
  } catch (err: any) {
    console.error("build-strategy error:", err);
    res.status(500).json({ error: err.message || "Failed to build strategy" });
  }
});

app.post("/api/build-interview", async (req, res) => {
  try {
    const { role, company, jobDescription, experience, location, resumeSummary, companyCulture } = req.body;
    const context = [
      `Target role: ${role}`,
      `Target company: ${company}`,
      location ? `Preferred location: ${location}` : "",
      `Experience level: ${experience}`,
      jobDescription ? `Job description:\n${jobDescription}` : "",
    ].filter(Boolean).join("\n");

    const user = `Prepare interview material and cover letters for this candidate.
${context}
Candidate summary: ${resumeSummary}
${companyCulture ? "Company culture: " + companyCulture : ""}`;

    const result = await generateJSON({
      system: `You are an interview coach and professional writer. Model answers should be strong and tailored.
STRICT JSON SCHEMA — use ONLY these exact keys:
{
  "questions": [{"category": "Technical"|"Behavioral"|"HR"|"Company-Specific", "difficulty": "Easy"|"Medium"|"Hard", "question": string, "modelAnswer": string, "explanation": string, "tip": string}],
  "coverLetters": {
    "atsOptimized": string,
    "companySpecific": string,
    "shortEmail": string,
    "premium": string
  }
}`,
      user,
      temperature: 0.6,
    });

    res.json(result);
  } catch (err: any) {
    console.error("build-interview error:", err);
    res.status(500).json({ error: err.message || "Failed to build interview prep" });
  }
});

app.post("/api/build-branding", async (req, res) => {
  try {
    const { role, company, jobDescription, experience, location, resumeSummary, candidateName } = req.body;
    const context = [
      `Target role: ${role}`,
      `Target company: ${company}`,
      location ? `Preferred location: ${location}` : "",
      `Experience level: ${experience}`,
      jobDescription ? `Job description:\n${jobDescription}` : "",
    ].filter(Boolean).join("\n");

    const user = `Create a personal branding and networking toolkit for this candidate.
${context}
Candidate name: ${candidateName ?? "the candidate"}
Candidate summary: ${resumeSummary}`;

    const result = await generateJSON({
      system: `You are a personal branding strategist and copywriter for tech professionals.
STRICT JSON SCHEMA — use ONLY these exact keys:
{
  "linkedin": {
    "headline": string, "about": string, "featured": [string], "skills": [string], "experienceRewrite": [string], "seoKeywords": [string]
  },
  "branding": {
    "linkedinPost": string, "websiteContent": string, "elevatorPitch": string, "professionalBio": string, "portfolioIntro": string, "twitterBio": string, "githubBio": string, "tagline": string
  },
  "networking": {
    "coldMessage": string, "connectionRequest": string, "referralRequest": string, "recruiterOutreach": string, "hiringManagerOutreach": string, "followUp": string, "thankYou": string
  }
}`,
      user,
      temperature: 0.7,
    });

    res.json(result);
  } catch (err: any) {
    console.error("build-branding error:", err);
    res.status(500).json({ error: err.message || "Failed to build branding" });
  }
});

// ─── Serve static in production ───────────────────────────────
const distPath = path.resolve(__dirname, "..", "dist");
app.use(express.static(distPath));
app.get("*", (_req, res) => {
  res.sendFile(path.join(distPath, "index.html"));
});

// ─── Start ────────────────────────────────────────────────────
const PORT = parseInt(process.env.PORT || "3001", 10);
app.listen(PORT, () => {
  console.log(`CareerForge AI server running on http://localhost:${PORT}`);
});
