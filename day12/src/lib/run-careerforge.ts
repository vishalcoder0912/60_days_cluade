import {
  callAnalyzeResume,
  callBuildBranding,
  callBuildInterview,
  callBuildStrategy,
  callRunResearch,
} from "./api";
import type { CareerInput, CareerReport } from "./types";

export const STEPS = [
  "Analyzing your resume",
  "Researching the company & role",
  "Building your skill-gap roadmap",
  "Preparing interviews & cover letters",
  "Crafting your personal brand kit",
] as const;

export type Progress = (stepIndex: number) => void;

export async function fileToBase64(file: File): Promise<string> {
  const buf = await file.arrayBuffer();
  let binary = "";
  const bytes = new Uint8Array(buf);
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) {
    binary += String.fromCharCode(...bytes.subarray(i, i + chunk));
  }
  return btoa(binary);
}

export async function runCareerForge(
  input: CareerInput,
  onProgress: Progress,
): Promise<CareerReport> {
  const base = {
    resumeText: input.resumeText,
    resumeFile: input.resumeFile,
    role: input.role,
    company: input.company,
    jobDescription: input.jobDescription,
    experience: input.experience,
    location: input.location,
  };

  onProgress(0);
  const analysis = await callAnalyzeResume(base);

  onProgress(1);
  const research = await callRunResearch(base);

  onProgress(2);
  const strategy = await callBuildStrategy({
    ...base,
    resumeSummary: analysis.resumeSummary,
    resumeSkills: analysis.skills,
    roleSkills: [
      ...research.role.requiredSkills,
      ...research.role.frequentSkills,
    ],
  });

  onProgress(3);
  const interview = await callBuildInterview({
    ...base,
    resumeSummary: analysis.resumeSummary,
    companyCulture: research.company.culture,
  });

  onProgress(4);
  const branding = await callBuildBranding({
    ...base,
    resumeSummary: analysis.resumeSummary,
    candidateName: analysis.candidateName,
  });

  return {
    input: {
      role: input.role,
      company: input.company,
      location: input.location,
      experience: input.experience,
    },
    analysis,
    research,
    strategy,
    interview,
    branding,
    generatedAt: new Date().toISOString(),
  };
}
