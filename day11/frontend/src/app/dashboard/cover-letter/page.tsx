"use client";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FileText, Loader2, Copy, Check } from "lucide-react";
import { resumeApi, jobApi, coverLetterApi } from "@/lib/api";

export default function CoverLetterPage() {
  const [resumes, setResumes] = useState<any[]>([]);
  const [jobs, setJobs] = useState<any[]>([]);
  const [form, setForm] = useState({ resume_id: "", job_description_id: "", company: "" });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    resumeApi.list().then((r) => setResumes(r.data)).catch(() => {});
    jobApi.list().then((r) => setJobs(r.data)).catch(() => {});
  }, []);

  const handleGenerate = async () => {
    setLoading(true); setError(""); setResult(null);
    try {
      const { data } = await coverLetterApi.generate(form);
      setResult(data);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Generation failed");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(result?.content || "");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="max-w-3xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">Cover Letter Generator</h1>
        <p className="text-muted-foreground mt-1 text-sm">Generate a personalized, job-specific cover letter (300-400 words).</p>
      </div>

      <div className="bg-card border border-border rounded-2xl p-6 mb-6">
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="text-sm font-medium text-foreground block mb-1.5">Resume</label>
            <select value={form.resume_id} onChange={(e) => setForm({ ...form, resume_id: e.target.value })}
              className="w-full bg-background border border-border rounded-lg px-3 py-2.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50">
              <option value="">Select resume...</option>
              {resumes.map((r: any) => <option key={r.id} value={r.id}>{r.filename}</option>)}
            </select>
          </div>
          <div>
            <label className="text-sm font-medium text-foreground block mb-1.5">Job Description</label>
            <select value={form.job_description_id} onChange={(e) => setForm({ ...form, job_description_id: e.target.value })}
              className="w-full bg-background border border-border rounded-lg px-3 py-2.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50">
              <option value="">Select job...</option>
              {jobs.map((j: any) => <option key={j.id} value={j.id}>{j.title || j.id.slice(0, 16)}</option>)}
            </select>
          </div>
        </div>
        <div className="mb-4">
          <label className="text-sm font-medium text-foreground block mb-1.5">Company Name (optional)</label>
          <input value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })}
            placeholder="e.g. Google"
            className="w-full bg-background border border-border rounded-lg px-3 py-2.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50" />
        </div>
        <button onClick={handleGenerate} disabled={!form.resume_id || !form.job_description_id || loading}
          className="flex items-center gap-2 bg-primary text-primary-foreground px-6 py-2.5 rounded-lg text-sm font-medium hover:opacity-90 disabled:opacity-50 transition-opacity">
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <FileText className="w-4 h-4" />}
          {loading ? "Writing cover letter..." : "Generate Cover Letter"}
        </button>
        {error && <p className="text-destructive text-sm mt-3">{error}</p>}
      </div>

      <AnimatePresence>
        {result && (
          <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="bg-card border border-border rounded-2xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-semibold text-foreground">Your Cover Letter</h2>
              <button onClick={handleCopy} className="flex items-center gap-2 text-xs text-muted-foreground hover:text-foreground transition-colors">
                {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? "Copied!" : "Copy"}
              </button>
            </div>
            <div className="bg-background border border-border rounded-xl p-5 text-sm text-foreground leading-relaxed whitespace-pre-wrap">
              {result.content}
            </div>
            <p className="text-xs text-muted-foreground mt-3">{result.content?.split(/\s+/).length || 0} words</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
