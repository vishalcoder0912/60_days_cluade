"use client";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Linkedin, Loader2, Sparkles } from "lucide-react";
import { resumeApi, linkedinApi } from "@/lib/api";

export default function LinkedInPage() {
  const [resumes, setResumes] = useState<any[]>([]);
  const [selectedResume, setSelectedResume] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    resumeApi.list().then((r) => setResumes(r.data)).catch(() => {});
  }, []);

  const handleOptimize = async () => {
    if (!selectedResume) return;
    setLoading(true); setError(""); setResult(null);
    try {
      const { data } = await linkedinApi.optimize(selectedResume);
      setResult(data);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Optimization failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">LinkedIn Optimizer</h1>
        <p className="text-muted-foreground mt-1 text-sm">
          Optimize your LinkedIn headline, about section, and experience descriptions.
        </p>
      </div>

      <div className="bg-card border border-border rounded-2xl p-6 mb-6">
        <div className="mb-4">
          <label className="text-sm font-medium text-foreground block mb-1.5">Select Resume</label>
          <select value={selectedResume} onChange={(e) => setSelectedResume(e.target.value)}
            className="w-full bg-background border border-border rounded-lg px-3 py-2.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50">
            <option value="">Choose a resume...</option>
            {resumes.map((r: any) => <option key={r.id} value={r.id}>{r.filename}</option>)}
          </select>
        </div>
        <button onClick={handleOptimize} disabled={!selectedResume || loading}
          className="flex items-center gap-2 bg-primary text-primary-foreground px-6 py-2.5 rounded-lg text-sm font-medium hover:opacity-90 disabled:opacity-50 transition-opacity">
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Linkedin className="w-4 h-4" />}
          {loading ? "Optimizing..." : "Optimize LinkedIn Profile"}
        </button>
        {error && <p className="text-destructive text-sm mt-3">{error}</p>}
      </div>

      <AnimatePresence>
        {result && (
          <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
            <div className="bg-card border border-border rounded-2xl p-6">
              <div className="flex items-center gap-2 mb-4">
                <Sparkles className="w-4 h-4 text-primary" />
                <h2 className="text-sm font-semibold text-foreground">Optimized Headline</h2>
              </div>
              <div className="bg-background border border-border rounded-xl p-4 text-sm text-foreground">
                {result.headline}
              </div>
            </div>

            <div className="bg-card border border-border rounded-2xl p-6">
              <div className="flex items-center gap-2 mb-4">
                <Sparkles className="w-4 h-4 text-primary" />
                <h2 className="text-sm font-semibold text-foreground">Optimized About Section</h2>
              </div>
              <div className="bg-background border border-border rounded-xl p-4 text-sm text-foreground leading-relaxed whitespace-pre-wrap">
                {result.about}
              </div>
            </div>

            {result.experience_rewrites?.length > 0 && (
              <div className="bg-card border border-border rounded-2xl p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Sparkles className="w-4 h-4 text-primary" />
                  <h2 className="text-sm font-semibold text-foreground">Experience Rewrites</h2>
                </div>
                {result.experience_rewrites.map((item: any, i: number) => (
                  <div key={i} className="mb-4 last:mb-0">
                    <div className="mb-2">
                      <span className="text-xs text-muted-foreground font-medium">Original:</span>
                      <p className="text-sm text-foreground bg-background border border-border rounded-lg p-3 mt-1">{item.original}</p>
                    </div>
                    <div>
                      <span className="text-xs text-muted-foreground font-medium">Optimized:</span>
                      <p className="text-sm text-foreground bg-primary/5 border border-primary/20 rounded-lg p-3 mt-1">{item.optimized}</p>
                    </div>
                    {i < result.experience_rewrites.length - 1 && <div className="border-t border-border my-4" />}
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
