"use client";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { History, FileText, Zap, Mail, FileText as CoverIcon, ArrowRight } from "lucide-react";
import Link from "next/link";
import { resumeApi, atsApi, coverLetterApi, coldEmailApi } from "@/lib/api";

export default function HistoryPage() {
  const [resumes, setResumes] = useState<any[]>([]);
  const [reports, setReports] = useState<any[]>([]);
  const [coverLetters, setCoverLetters] = useState<any[]>([]);
  const [coldEmails, setColdEmails] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState("ats");

  useEffect(() => {
    resumeApi.list().then((r) => setResumes(r.data)).catch(() => {});
    atsApi.listReports().then((r) => setReports(r.data)).catch(() => {});
    coverLetterApi.list().then((r) => setCoverLetters(r.data)).catch(() => {});
    coldEmailApi.list().then((r) => setColdEmails(r.data)).catch(() => {});
  }, []);

  const tabs = [
    { key: "ats", label: "ATS Reports", count: reports.length, icon: Zap },
    { key: "cover", label: "Cover Letters", count: coverLetters.length, icon: CoverIcon },
    { key: "email", label: "Cold Emails", count: coldEmails.length, icon: Mail },
    { key: "resume", label: "Resumes", count: resumes.length, icon: FileText },
  ];

  return (
    <div className="max-w-4xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">History</h1>
        <p className="text-muted-foreground mt-1 text-sm">View all your generated content and reports.</p>
      </div>

      <div className="flex gap-1 bg-card border border-border rounded-xl p-1 mb-6 w-fit">
        {tabs.map((t) => (
          <button key={t.key} onClick={() => setActiveTab(t.key)}
            className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              activeTab === t.key ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
            }`}>
            <t.icon className="w-3.5 h-3.5" />
            {t.label}
            <span className={`text-xs ${activeTab === t.key ? "text-primary-foreground/70" : "text-muted-foreground"}`}>
              {t.count}
            </span>
          </button>
        ))}
      </div>

      <motion.div key={activeTab} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
        {activeTab === "ats" && (
          <div className="space-y-2">
            {reports.length === 0 && <p className="text-sm text-muted-foreground py-8 text-center">No ATS reports yet.</p>}
            {reports.map((r: any) => (
              <div key={r.id} className="flex items-center justify-between bg-card border border-border rounded-xl px-5 py-3.5">
                <div>
                  <div className="text-sm text-foreground font-medium">ATS Report</div>
                  <div className="text-xs text-muted-foreground">{new Date(r.created_at).toLocaleDateString()}</div>
                </div>
                <div className="flex items-center gap-3">
                  <div className={`text-lg font-bold ${r.ats_score >= 80 ? "text-green-400" : r.ats_score >= 60 ? "text-yellow-400" : "text-red-400"}`}>
                    {r.ats_score}%
                  </div>
                  <Link href={`/dashboard/ats-score?report=${r.id}`} className="text-xs text-primary hover:underline">View</Link>
                </div>
              </div>
            ))}
            {reports.length > 0 && <Link href="/dashboard/ats-score" className="text-xs text-primary hover:underline block text-center mt-4">Generate new ATS score →</Link>}
          </div>
        )}

        {activeTab === "cover" && (
          <div className="space-y-2">
            {coverLetters.length === 0 && <p className="text-sm text-muted-foreground py-8 text-center">No cover letters yet.</p>}
            {coverLetters.map((c: any) => (
              <div key={c.id} className="bg-card border border-border rounded-xl px-5 py-3.5">
                <div className="flex items-center justify-between mb-1">
                  <div className="text-sm text-foreground font-medium">{c.company || "Cover Letter"}</div>
                  <div className="text-xs text-muted-foreground">{new Date(c.created_at).toLocaleDateString()}</div>
                </div>
                <p className="text-xs text-muted-foreground line-clamp-2">{c.content?.slice(0, 200)}...</p>
              </div>
            ))}
            {coverLetters.length > 0 && <Link href="/dashboard/cover-letter" className="text-xs text-primary hover:underline block text-center mt-4">Generate new cover letter →</Link>}
          </div>
        )}

        {activeTab === "email" && (
          <div className="space-y-2">
            {coldEmails.length === 0 && <p className="text-sm text-muted-foreground py-8 text-center">No cold emails yet.</p>}
            {coldEmails.map((e: any) => (
              <div key={e.id} className="bg-card border border-border rounded-xl px-5 py-3.5">
                <div className="flex items-center justify-between mb-1">
                  <div className="text-sm text-foreground font-medium">{e.subject}</div>
                  <div className="text-xs text-muted-foreground">{new Date(e.created_at).toLocaleDateString()}</div>
                </div>
                <p className="text-xs text-muted-foreground">To: {e.recruiter_email} · {e.company}</p>
              </div>
            ))}
            {coldEmails.length > 0 && <Link href="/dashboard/cold-email" className="text-xs text-primary hover:underline block text-center mt-4">Generate new cold email →</Link>}
          </div>
        )}

        {activeTab === "resume" && (
          <div className="space-y-2">
            {resumes.length === 0 && <p className="text-sm text-muted-foreground py-8 text-center">No resumes uploaded yet.</p>}
            {resumes.map((r: any) => (
              <div key={r.id} className="flex items-center justify-between bg-card border border-border rounded-xl px-5 py-3.5">
                <div>
                  <div className="text-sm text-foreground font-medium">{r.filename}</div>
                  <div className="text-xs text-muted-foreground">{new Date(r.created_at).toLocaleDateString()}</div>
                </div>
                <FileText className="w-4 h-4 text-muted-foreground" />
              </div>
            ))}
            {resumes.length > 0 && <Link href="/dashboard/upload-resume" className="text-xs text-primary hover:underline block text-center mt-4">Upload new resume →</Link>}
          </div>
        )}
      </motion.div>
    </div>
  );
}
