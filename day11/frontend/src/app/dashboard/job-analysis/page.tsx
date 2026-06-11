"use client";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Briefcase, Loader2, CheckCircle2 } from "lucide-react";
import { jobApi } from "@/lib/api";

export default function JobAnalysisPage() {
  const [text, setText] = useState("");
  const [company, setCompany] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!text.trim() || text.length < 50) return;
    setLoading(true);
    setError("");
    try {
      const { data } = await jobApi.analyze({ text, company });
      setResult(data);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">Job Description Analysis</h1>
        <p className="text-muted-foreground mt-1 text-sm">
          Paste a job description and AI will extract keywords, skills, and requirements.
        </p>
      </div>

      <div className="bg-card border border-border rounded-2xl p-6 mb-6">
        <div className="mb-4">
          <label className="text-sm font-medium text-foreground block mb-1.5">Company Name (optional)</label>
          <input value={company} onChange={(e) => setCompany(e.target.value)}
            placeholder="e.g. Google, Microsoft, Startup Inc."
            className="w-full bg-background border border-border rounded-lg px-3 py-2.5 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50" />
        </div>
        <div className="mb-4">
          <label className="text-sm font-medium text-foreground block mb-1.5">
            Job Description <span className="text-destructive">*</span>
          </label>
          <textarea value={text} onChange={(e) => setText(e.target.value)}
            placeholder="Paste the full job description here..." rows={12}
            className="w-full bg-background border border-border rounded-lg px-3 py-2.5 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 resize-none font-mono" />
          <p className="text-xs text-muted-foreground mt-1">{text.length} chars · min 50 required</p>
        </div>
        <button onClick={handleAnalyze} disabled={loading || text.length < 50}
          className="flex items-center gap-2 bg-primary text-primary-foreground px-6 py-2.5 rounded-lg text-sm font-medium hover:opacity-90 disabled:opacity-50 transition-opacity">
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Briefcase className="w-4 h-4" />}
          {loading ? "Analyzing with AI..." : "Analyze Job Description"}
        </button>
        {error && <p className="text-destructive text-sm mt-3">{error}</p>}
      </div>

      <AnimatePresence>
        {result && (
          <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="bg-card border border-border rounded-2xl p-6">
            <div className="flex items-center gap-2 mb-5">
              <CheckCircle2 className="w-5 h-5 text-green-400" />
              <span className="text-sm font-semibold text-foreground">Job saved · Analysis in progress</span>
            </div>
            <p className="text-xs text-muted-foreground mb-5">
              ID: <code className="font-mono bg-muted px-2 py-0.5 rounded">{result.id}</code> — use this when generating ATS scores and cover letters.
            </p>
            <div className="bg-background border border-border rounded-lg p-4 text-sm text-green-400 font-medium">
              Job description queued for AI analysis. Navigate to ATS Score to proceed.
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
