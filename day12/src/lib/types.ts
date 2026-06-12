export type Experience =
  | "Intern"
  | "Entry"
  | "Mid"
  | "Senior"
  | "Lead"
  | "Executive";

export interface CareerInput {
  resumeText?: string;
  resumeFile?: { name: string; mime: string; dataBase64: string };
  role: string;
  company: string;
  jobDescription?: string;
  experience: Experience;
  location?: string;
}

export interface ResumeAnalysis {
  resumeSummary: string;
  candidateName: string;
  atsScore: number;
  resumeHealth: number;
  skills: string[];
  education: string[];
  certifications: string[];
  projects: { name: string; description: string }[];
  workExperience: { title: string; org: string; highlights: string[] }[];
  keywords: string[];
  missingKeywords: string[];
  missingSkills: string[];
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
  keywordMatch: { keyword: string; present: boolean }[];
}

export interface CompanyReport {
  overview: string;
  mission: string;
  values: string[];
  recentNews: string[];
  productLaunches: string[];
  funding: string;
  leadership: { name: string; role: string }[];
  hiringTrends: string;
  techStack: string[];
  culture: string;
  interviewExperiences: string[];
  competitors: string[];
}

export interface RoleReport {
  requiredSkills: string[];
  frequentSkills: string[];
  tools: string[];
  technologies: string[];
  certifications: string[];
  responsibilities: string[];
  salaryInsights: string;
  careerGrowth: string[];
}

export interface ResearchResult {
  company: CompanyReport;
  role: RoleReport;
  sources: { title: string; url: string }[];
}

export interface LearningItem {
  skill: string;
  why: string;
  course: string;
  youtube: string;
  documentation: string;
  practice: string;
  projectIdea: string;
}

export interface StrategyResult {
  matchingSkills: string[];
  missingSkills: string[];
  matchPercent: number;
  plan30: string[];
  plan60: string[];
  plan90: string[];
  learning: LearningItem[];
}

export interface InterviewQuestion {
  category: "Technical" | "Behavioral" | "HR" | "Company-Specific";
  difficulty: "Easy" | "Medium" | "Hard";
  question: string;
  modelAnswer: string;
  explanation: string;
  tip: string;
}

export interface InterviewResult {
  questions: InterviewQuestion[];
  coverLetters: {
    atsOptimized: string;
    companySpecific: string;
    shortEmail: string;
    premium: string;
  };
}

export interface BrandingResult {
  linkedin: {
    headline: string;
    about: string;
    featured: string[];
    skills: string[];
    experienceRewrite: string[];
    seoKeywords: string[];
  };
  branding: {
    linkedinPost: string;
    websiteContent: string;
    elevatorPitch: string;
    professionalBio: string;
    portfolioIntro: string;
    twitterBio: string;
    githubBio: string;
    tagline: string;
  };
  networking: {
    coldMessage: string;
    connectionRequest: string;
    referralRequest: string;
    recruiterOutreach: string;
    hiringManagerOutreach: string;
    followUp: string;
    thankYou: string;
  };
}

export interface CareerReport {
  input: {
    role: string;
    company: string;
    location?: string;
    experience: Experience;
  };
  analysis: ResumeAnalysis;
  research: ResearchResult;
  strategy: StrategyResult;
  interview: InterviewResult;
  branding: BrandingResult;
  generatedAt: string;
}
