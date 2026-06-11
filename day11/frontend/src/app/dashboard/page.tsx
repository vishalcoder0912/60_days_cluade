"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Upload, Briefcase, Zap, FileText, Mail, ArrowRight, TrendingUp } from "lucide-react";
import { resumeApi, atsApi } from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";

const quickActions = [
  { href: "/dashboard/upload-resume", icon: Upload, label: "Upload Resume", desc: "Add a new resume", color: "text-blue-400" },
  { href: "/dashboard/job-analysis", icon: Briefcase, label: "Analyze Job", desc: "Paste a job description", color: "text-green-400" },
  { href: "/dashboard/ats-score", icon: Zap, label: "Get ATS Score", desc: "Score resume vs job", color: "text-yellow-400" },
  { href: "/dashboard/cover-letter", icon: FileText, label: "Cover Letter", desc: "Generate personalized letter", color: "text-purple-400" },
  { href: "/dashboard/cold-email", icon: Mail, label: "Cold Email", desc: "Reach out to recruiters", color: "text-pink-400" },
];

export default function DashboardPage() {
  const { user } = useAuth();
  const [resumes, setResumes] = useState<any[]>([]);
  const [reports, setReports] = useState<any[]>([]);

  useEffect(() => {
    resumeApi.list().then((r) => setResumes(r.data)).catch(() => {});
    atsApi.listReports().then((r) => setReports(r.data)).catch(() => {});
  }, []);

  const avgScore = reports.length
    ? Math.round(reports.reduce((s, r) => s + r.ats_score, 0) / reports.length)
    : null;

  return (
    <div className="max-w-5xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">
          Good {new Date().getHours() < 12 ? "morning" : "afternoon"}, {user?.name?.split(" ")[0]}
        </h1>
        <p className="text-muted-foreground mt-1">Here's your job application overview.</p>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-8">
        {[
          { label: "Resumes", value: resumes.length, icon: Upload },
          { label: "ATS Reports", value: reports.length, icon: Zap },
          { label: "Avg ATS Score", value: avgScore !== null ? `${avgScore}%` : "-", icon: TrendingUp },
        ].map((s, i) => (
          <motion.div key={s.label} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 * i }}
            className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm text-muted-foreground">{s.label}</span>
              <s.icon className="w-4 h-4 text-muted-foreground" />
            </div>
            <div className="text-3xl font-bold text-foreground">{s.value}</div>
          </motion.div>
        ))}
      </div>

      <h2 className="text-base font-semibold text-foreground mb-4">Quick Actions</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-8">
        {quickActions.map((a, i) => (
          <motion.div key={a.href} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 * i }}>
            <Link href={a.href}
              className="group flex items-center gap-4 bg-card border border-border rounded-xl p-4 hover:border-primary/40 transition-all">
              <div className="w-9 h-9 rounded-lg bg-accent flex items-center justify-center group-hover:bg-primary/10 transition-colors">
                <a.icon className={`w-4 h-4 ${a.color}`} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-foreground">{a.label}</div>
                <div className="text-xs text-muted-foreground truncate">{a.desc}</div>
              </div>
              <ArrowRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
            </Link>
          </motion.div>
        ))}
      </div>

      {reports.length > 0 && (
        <div>
          <h2 className="text-base font-semibold text-foreground mb-4">Recent ATS Reports</h2>
          <div className="space-y-2">
            {reports.slice(0, 5).map((r: any) => (
              <div key={r.id} className="flex items-center justify-between bg-card border border-border rounded-xl px-5 py-3.5">
                <div className="text-sm text-foreground">{r.id.slice(0, 8)}...</div>
                <div className="flex items-center gap-3">
                  <div className={`text-lg font-bold ${r.ats_score >= 80 ? "text-green-400" : r.ats_score >= 60 ? "text-yellow-400" : "text-red-400"}`}>
                    {r.ats_score}%
                  </div>
                  <Link href={`/dashboard/ats-score?report=${r.id}`} className="text-xs text-primary hover:underline">View</Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {resumes.length === 0 && (
        <div className="text-center py-16 bg-card border border-dashed border-border rounded-2xl">
          <Upload className="w-10 h-10 text-muted-foreground mx-auto mb-3" />
          <h3 className="font-medium text-foreground mb-1">Upload your first resume</h3>
          <p className="text-sm text-muted-foreground mb-4">Start by uploading a PDF, DOCX, or TXT resume</p>
          <Link href="/dashboard/upload-resume"
            className="inline-flex items-center gap-2 bg-primary text-primary-foreground px-5 py-2 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity">
            <Upload className="w-4 h-4" /> Upload Resume
          </Link>
        </div>
      )}
    </div>
  );
}
