import type {
  CareerInput,
  ResumeAnalysis,
  ResearchResult,
  StrategyResult,
  InterviewResult,
  BrandingResult,
} from "./types";

export async function callAnalyzeResume(
  input: CareerInput,
): Promise<ResumeAnalysis> {
  const res = await fetch("/api/analyze-resume", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: "Request failed" }));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function callRunResearch(
  input: CareerInput,
): Promise<ResearchResult> {
  const res = await fetch("/api/research", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: "Request failed" }));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function callBuildStrategy(input: {
  role: string;
  company: string;
  jobDescription?: string;
  experience: string;
  location?: string;
  resumeSummary: string;
  resumeSkills: string[];
  roleSkills: string[];
}): Promise<StrategyResult> {
  const res = await fetch("/api/build-strategy", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: "Request failed" }));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function callBuildInterview(input: {
  role: string;
  company: string;
  jobDescription?: string;
  experience: string;
  location?: string;
  resumeSummary: string;
  companyCulture?: string;
}): Promise<InterviewResult> {
  const res = await fetch("/api/build-interview", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: "Request failed" }));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function callBuildBranding(input: {
  role: string;
  company: string;
  jobDescription?: string;
  experience: string;
  location?: string;
  resumeSummary: string;
  candidateName?: string;
}): Promise<BrandingResult> {
  const res = await fetch("/api/build-branding", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: "Request failed" }));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}
