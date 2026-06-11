"use client";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageSquare, Loader2, CheckCircle2 } from "lucide-react";
import { resumeApi, jobApi, interviewApi } from "@/lib/api";

export default function InterviewPrepPage() {
  const [resumes, setResumes] = useState<any[]>([]);
  const [jobs, setJobs] = useState<any[]>([]);
  const [selectedResume, setSelectedResume] = useState("");
  const [selectedJob, setSelectedJob] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    resumeApi.list().then((r) => setResumes(r.data)).catch(() => {});
    jobApi.list().then((r) => setJobs(r.data)).catch(() => {});
  }, []);

  const handleGenerate = async () => {
    if (!selectedResume || !selectedJob) return;
    setLoading(true); setError(""); setResult(null);
    try {
      const { data } = await interviewApi.questions({ resume_id: selectedResume, job_description_id: selectedJob });
      setResult(data);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Failed to generate questions");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">Interview Preparation</h1>
        <p className="text-muted-foreground mt-1 text-sm">
          Generate technical, behavioral, and HR questions based on your resume and the job description.
        </p>
      </div>

      <div className="bg-card border border-border rounded-2xl p-6 mb-6">
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="text-sm font-medium text-foreground block mb-1.5">Resume</label>
            <select value={selectedResume} onChange={(e) => setSelectedResume(e.target.value)}
              className="w-full bg-background border border-border rounded-lg px-3 py-2.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50">
              <option value="">Select resume...</option>
              {resumes.map((r: any) => <option key={r.id} value={r.id}>{r.filename}</option>)}
            </select>
          </div>
          <div>
            <label className="text-sm font-medium text-foreground block mb-1.5">Job Description</label>
            <select value={selectedJob} onChange={(e) => setSelectedJob(e.target.value)}
              className="w-full bg-background border border-border rounded-lg px-3 py-2.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50">
              <option value="">Select job...</option>
              {jobs.map((j: any) => <option key={j.id} value={j.id}>{j.title || j.id.slice(0, 16)}</option>)}
            </select>
          </div>
        </div>
        <button onClick={handleGenerate} disabled={!selectedResume || !selectedJob || loading}
          className="flex items-center gap-2 bg-primary text-primary-foreground px-6 py-2.5 rounded-lg text-sm font-medium hover:opacity-90 disabled:opacity-50 transition-opacity">
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <MessageSquare className="w-4 h-4" />}
          {loading ? "Generating questions..." : "Generate Interview Questions"}
        </button>
        {error && <p className="text-destructive text-sm mt-3">{error}</p>}
      </div>

      <AnimatePresence>
        {result && (
          <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
            {[
              { title: "Technical Questions", items: result.technical, color: "text-blue-400" },
              { title: "HR Questions", items: result.hr, color: "text-green-400" },
              { title: "Behavioral Questions (STAR)", items: result.behavioral, color: "text-purple-400" },
            ].filter((s) => s.items?.length > 0).map((section) => (
              <div key={section.title} className="bg-card border border-border rounded-2xl p-6">
                <h2 className="text-sm font-semibold text-foreground mb-4">{section.title}</h2>
                <div className="space-y-3">
                  {section.items.map((q: string, i: number) => (
                    <div key={i} className="flex items-start gap-3">
                      <CheckCircle2 className={`w-4 h-4 ${section.color} flex-shrink-0 mt-0.5`} />
                      <span className="text-sm text-foreground">{q}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
