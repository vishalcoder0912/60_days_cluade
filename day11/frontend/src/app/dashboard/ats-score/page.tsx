"use client";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Zap, Loader2, CheckCircle2, AlertTriangle, Download } from "lucide-react";
import { resumeApi, jobApi, atsApi } from "@/lib/api";

function ScoreRing({ score, label }: { score: number; label: string }) {
  const r = 54;
  const circ = 2 * Math.PI * r;
  const offset = circ - (score / 100) * circ;
  const color = score >= 80 ? "#4ade80" : score >= 60 ? "#facc15" : "#f87171";

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="128" height="128" viewBox="0 0 128 128">
        <circle cx="64" cy="64" r={r} fill="none" stroke="hsl(var(--border))" strokeWidth="8" />
        <motion.circle cx="64" cy="64" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeLinecap="round" strokeDasharray={circ}
          initial={{ strokeDashoffset: circ }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.2, ease: "easeOut" }}
          transform="rotate(-90 64 64)" />
        <text x="64" y="60" textAnchor="middle" fontSize="22" fontWeight="bold" className="fill-foreground">
          {score}
        </text>
        <text x="64" y="78" textAnchor="middle" fontSize="11" className="fill-muted-foreground">
          / 100
        </text>
      </svg>
      <span className="text-xs text-muted-foreground font-medium">{label}</span>
    </div>
  );
}

export default function ATSScorePage() {
  const [resumes, setResumes] = useState<any[]>([]);
  const [jobs, setJobs] = useState<any[]>([]);
  const [selectedResume, setSelectedResume] = useState("");
  const [selectedJob, setSelectedJob] = useState("");
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState<any>(null);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState<"scores" | "optimize" | "suggestions">("scores");
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    resumeApi.list().then((r) => setResumes(r.data)).catch(() => {});
    jobApi.list().then((r) => setJobs(r.data)).catch(() => {});
  }, []);

  const handleScore = async () => {
    if (!selectedResume || !selectedJob) return;
    setLoading(true);
    setError("");
    setReport(null);
    try {
      const { data } = await atsApi.score({ resume_id: selectedResume, job_description_id: selectedJob });
      setReport(data);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Scoring failed");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!report?.id) return;
    setDownloading(true);
    try {
      const response = await atsApi.downloadOptimized(report.id);
      const blob = new Blob([response.data], { type: "text/plain" });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `optimized_resume_${report.id.slice(0, 8)}.txt`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (e) {
      console.error("Download failed:", e);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="max-w-4xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">ATS Score</h1>
        <p className="text-muted-foreground mt-1 text-sm">Analyze how well your resume matches a job description.</p>
      </div>

      <div className="bg-card border border-border rounded-2xl p-6 mb-6">
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="text-sm font-medium text-foreground block mb-1.5">Select Resume</label>
            <select value={selectedResume} onChange={(e) => setSelectedResume(e.target.value)}
              className="w-full bg-background border border-border rounded-lg px-3 py-2.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50">
              <option value="">Choose a resume...</option>
              {resumes.map((r: any) => <option key={r.id} value={r.id}>{r.filename}</option>)}
            </select>
          </div>
          <div>
            <label className="text-sm font-medium text-foreground block mb-1.5">Select Job Description</label>
            <select value={selectedJob} onChange={(e) => setSelectedJob(e.target.value)}
              className="w-full bg-background border border-border rounded-lg px-3 py-2.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50">
              <option value="">Choose a job...</option>
              {jobs.map((j: any) => <option key={j.id} value={j.id}>{j.title || j.id.slice(0, 16)}</option>)}
            </select>
          </div>
        </div>
        <button onClick={handleScore} disabled={!selectedResume || !selectedJob || loading}
          className="flex items-center gap-2 bg-primary text-primary-foreground px-6 py-2.5 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-50">
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Zap className="w-4 h-4" />}
          {loading ? "Analyzing with AI..." : "Calculate ATS Score"}
        </button>
        {loading && <p className="text-xs text-muted-foreground mt-3">This may take 30-90 seconds...</p>}
        {error && <p className="text-destructive text-sm mt-3">{error}</p>}
      </div>

      {report && (
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}>
          <div className="bg-card border border-border rounded-2xl p-8 mb-4">
            <div className="flex flex-col items-center mb-8">
              <ScoreRing score={Math.round(report.ats_score)} label="Overall ATS Score" />
              <p className="text-sm text-muted-foreground mt-3 text-center max-w-sm">
                {report.ats_score >= 80
                  ? "Excellent! Your resume is well-optimized for this role."
                  : report.ats_score >= 60
                  ? "Good. Some improvements can boost your chances."
                  : "Needs work. Optimize your resume to pass ATS filters."}
              </p>
            </div>
            <div className="grid grid-cols-3 gap-3">
              {[
                { label: "Keywords", score: report.keyword_match, weight: "30%" },
                { label: "Skills", score: report.skill_match, weight: "20%" },
                { label: "Experience", score: report.experience_match, weight: "20%" },
                { label: "Education", score: report.education_match, weight: "10%" },
                { label: "Formatting", score: report.formatting, weight: "10%" },
                { label: "Readability", score: report.readability, weight: "10%" },
              ].map((item) => (
                <div key={item.label} className="bg-background border border-border rounded-xl p-4">
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-xs text-muted-foreground">{item.label}</span>
                    <span className="text-xs text-muted-foreground">{item.weight}</span>
                  </div>
                  <div className={`text-2xl font-bold ${item.score >= 80 ? "text-green-400" : item.score >= 60 ? "text-yellow-400" : "text-red-400"}`}>
                    {Math.round(item.score)}
                  </div>
                  <div className="mt-2 h-1.5 bg-border rounded-full overflow-hidden">
                    <motion.div className={`h-full rounded-full ${item.score >= 80 ? "bg-green-400" : item.score >= 60 ? "bg-yellow-400" : "bg-red-400"}`}
                      initial={{ width: 0 }} animate={{ width: `${item.score}%` }} transition={{ duration: 0.8, delay: 0.2 }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="flex gap-1 bg-card border border-border rounded-xl p-1 mb-4 w-fit">
            {(["scores", "optimize", "suggestions"] as const).map((t) => (
              <button key={t} onClick={() => setActiveTab(t)}
                className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors capitalize ${
                  activeTab === t ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
                }`}>
                {t === "optimize" ? "Optimized Resume" : t}
              </button>
            ))}
          </div>

          {activeTab === "scores" && (
            <div className="grid grid-cols-2 gap-4">
              {report.missing_keywords?.length > 0 && (
                <div className="bg-card border border-border rounded-xl p-5">
                  <h3 className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-yellow-400" /> Missing Keywords
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {report.missing_keywords.map((k: string) => (
                      <span key={k} className="text-xs bg-yellow-400/10 text-yellow-400 border border-yellow-400/20 px-2.5 py-1 rounded-full">{k}</span>
                    ))}
                  </div>
                </div>
              )}
              {report.missing_skills?.length > 0 && (
                <div className="bg-card border border-border rounded-xl p-5">
                  <h3 className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-red-400" /> Missing Skills
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {report.missing_skills.map((s: string) => (
                      <span key={s} className="text-xs bg-red-400/10 text-red-400 border border-red-400/20 px-2.5 py-1 rounded-full">{s}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === "suggestions" && report.suggestions?.length > 0 && (
            <div className="bg-card border border-border rounded-xl p-5 space-y-3">
              <h3 className="text-sm font-semibold text-foreground mb-4">Improvement Suggestions</h3>
              {report.suggestions.map((s: string, i: number) => (
                <div key={i} className="flex items-start gap-3 text-sm text-muted-foreground">
                  <CheckCircle2 className="w-4 h-4 text-primary flex-shrink-0 mt-0.5" />
                  {s}
                </div>
              ))}
            </div>
          )}

          {activeTab === "optimize" && report.optimized_resume && (
            <div className="bg-card border border-border rounded-xl p-5">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-semibold text-foreground">AI-Optimized Resume</h3>
                <div className="flex gap-3">
                  <button onClick={() => navigator.clipboard.writeText(report.optimized_resume)}
                    className="text-xs text-primary hover:underline">Copy to clipboard</button>
                  <button onClick={handleDownload} disabled={downloading}
                    className="flex items-center gap-1.5 text-xs bg-primary text-primary-foreground px-3 py-1.5 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50">
                    {downloading ? <Loader2 className="w-3 h-3 animate-spin" /> : <Download className="w-3 h-3" />}
                    Download
                  </button>
                </div>
              </div>
              <pre className="text-xs text-muted-foreground whitespace-pre-wrap font-mono bg-background rounded-lg p-4 max-h-96 overflow-y-auto">
                {report.optimized_resume}
              </pre>
            </div>
          )}
        </motion.div>
      )}
    </div>
  );
}
