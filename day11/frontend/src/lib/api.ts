import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

export const resumeApi = {
  upload: (file: File) => {
    const fd = new FormData();
    fd.append("file", file);
    return api.post("/api/resume/upload", fd, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  list: () => api.get("/api/resume/"),
  get: (id: string) => api.get(`/api/resume/${id}`),
  delete: (id: string) => api.delete(`/api/resume/${id}`),
};

export const jobApi = {
  analyze: (data: { text: string; company?: string; source_url?: string }) =>
    api.post("/api/job/analyze", data),
  list: () => api.get("/api/job/"),
  get: (id: string) => api.get(`/api/job/${id}`),
};

export const atsApi = {
  score: (data: { resume_id: string; job_description_id: string }) =>
    api.post("/api/ats/score", data),
  listReports: () => api.get("/api/ats/reports"),
  getReport: (id: string) => api.get(`/api/ats/reports/${id}`),
  downloadOptimized: (reportId: string) =>
    api.get(`/api/ats/reports/${reportId}/download`, { responseType: "blob" }),
};

export const coverLetterApi = {
  generate: (data: { resume_id: string; job_description_id: string; company?: string }) =>
    api.post("/api/cover-letter/", data),
  list: () => api.get("/api/cover-letter/"),
};

export const coldEmailApi = {
  generate: (data: {
    resume_id: string;
    job_description_id: string;
    recruiter_email: string;
    company: string;
  }) => api.post("/api/cold-email/", data),
  list: () => api.get("/api/cold-email/"),
};

export const linkedinApi = {
  optimize: (resume_id: string) =>
    api.post("/api/linkedin/optimize", { resume_id }),
};

export const interviewApi = {
  questions: (data: { resume_id: string; job_description_id: string }) =>
    api.post("/api/interview/questions", data),
};
