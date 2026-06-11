export interface User {
  id: string;
  name: string;
  email: string;
}

export interface Resume {
  id: string;
  filename: string;
  file_path: string;
  raw_text?: string;
  parsed_data?: ParsedResume;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface ParsedResume {
  name?: string;
  email?: string;
  phone?: string;
  linkedin?: string;
  github?: string;
  summary?: string;
  skills: string[];
  experience: Experience[];
  education: Education[];
  projects: Project[];
  certifications: string[];
  achievements: string[];
}

export interface Experience {
  title: string;
  company: string;
  duration: string;
  description: string;
}

export interface Education {
  degree: string;
  institution: string;
  year: string;
}

export interface Project {
  name: string;
  description: string;
  technologies: string[];
}

export interface JobDescription {
  id: string;
  title?: string;
  company?: string;
  raw_text: string;
  parsed_data?: ParsedJob;
  created_at: string;
}

export interface ParsedJob {
  job_title: string;
  company: string;
  required_skills: string[];
  preferred_skills: string[];
  keywords: string[];
  experience: string;
  education: string;
  responsibilities: string[];
}

export interface ATSReport {
  id: string;
  ats_score: number;
  keyword_match: number;
  skill_match: number;
  experience_match: number;
  education_match: number;
  formatting: number;
  readability: number;
  missing_keywords: string[];
  missing_skills: string[];
  suggestions: string[];
  optimized_resume?: string;
  created_at: string;
}

export interface CoverLetter {
  id: string;
  content: string;
  company?: string;
  created_at: string;
}

export interface ColdEmail {
  id: string;
  subject: string;
  body: string;
  recruiter_email: string;
  company: string;
  created_at: string;
}

export interface InterviewQuestions {
  technical: string[];
  hr: string[];
  behavioral: string[];
}

export interface LinkedInOptimization {
  headline: string;
  about: string;
  experience_rewrites: { original: string; optimized: string }[];
}
