"use client";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  FileText, Zap, Mail, Linkedin, BrainCircuit,
  ArrowRight, CheckCircle2, Star
} from "lucide-react";

const features = [
  { icon: FileText, title: "Resume Upload & Parse", desc: "Upload PDF, DOCX, or TXT. AI extracts all your details automatically." },
  { icon: Zap, title: "ATS Score Engine", desc: "Know exactly how your resume scores against any job description." },
  { icon: BrainCircuit, title: "AI Optimization", desc: "Rewrite and optimize your resume with FAANG-level AI — without fabricating anything." },
  { icon: FileText, title: "Cover Letter Generator", desc: "Personalized 300-word cover letters that actually get read." },
  { icon: Mail, title: "Cold Email Generator", desc: "Reach recruiters directly with compelling outreach emails." },
  { icon: Linkedin, title: "LinkedIn Optimizer", desc: "Transform your profile headline and about section for maximum visibility." },
];

const stats = [
  { value: "3x", label: "More interviews" },
  { value: "92%", label: "Avg ATS score" },
  { value: "100%", label: "Free to run" },
  { value: "Cloud", label: "AI — OpenRouter free" },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b border-border/50 px-6 py-4 flex items-center justify-between max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-primary flex items-center justify-center">
            <Zap className="w-4 h-4 text-primary-foreground" />
          </div>
          <span className="font-semibold text-foreground">ATS Optimizer</span>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/dashboard" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            Dashboard
          </Link>
          <Link
            href="/dashboard"
            className="text-sm bg-primary text-primary-foreground px-4 py-2 rounded-lg hover:opacity-90 transition-opacity font-medium"
          >
            Get Started
          </Link>
        </div>
      </nav>

      <section className="max-w-7xl mx-auto px-6 pt-24 pb-16 text-center">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <div className="inline-flex items-center gap-2 bg-primary/10 text-primary border border-primary/20 rounded-full px-4 py-1.5 text-sm mb-8">
            <Star className="w-3.5 h-3.5" />
            Powered by Google Gemma 4 (Free) · No paid API required
          </div>
          <h1 className="text-5xl md:text-7xl font-bold text-foreground leading-tight mb-6">
            Land more interviews
            <br />
            <span className="text-primary">with AI-optimized</span>
            <br />
            resumes
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10">
            ATS score your resume, optimize it for any job, generate cover letters and cold emails —
            all running locally on your machine. Free forever.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/dashboard"
              className="flex items-center gap-2 bg-primary text-primary-foreground px-8 py-3.5 rounded-xl text-base font-semibold hover:opacity-90 transition-opacity glow-primary"
            >
              Start Optimizing <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              href="/dashboard"
              className="flex items-center gap-2 border border-border text-foreground px-8 py-3.5 rounded-xl text-base font-medium hover:bg-accent transition-colors"
            >
              View Dashboard
            </Link>
          </div>
        </motion.div>
      </section>

      <section className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {stats.map((s, i) => (
            <motion.div
              key={s.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * i }}
              className="bg-card border border-border rounded-xl p-6 text-center"
            >
              <div className="text-3xl font-bold text-primary mb-1">{s.value}</div>
              <div className="text-sm text-muted-foreground">{s.label}</div>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-6 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-foreground mb-3">Everything you need to get hired</h2>
          <p className="text-muted-foreground">Powered by OpenRouter + Google Gemma 4 (free models)</p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {features.map((f, i) => (
            <motion.div
              key={f.title} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.05 * i }}
              className="bg-card border border-border rounded-xl p-6 hover:border-primary/40 transition-colors"
            >
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <f.icon className="w-5 h-5 text-primary" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">{f.title}</h3>
              <p className="text-sm text-muted-foreground">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-6 py-16">
        <div className="bg-card border border-border rounded-2xl p-8">
          <h2 className="text-2xl font-bold text-foreground mb-6">Get running in 5 minutes</h2>
          <div className="space-y-4">
            {[
              { step: "1", title: "Install dependencies", cmd: "npm run install:all" },
              { step: "2", title: "Start the app", cmd: "npm run dev" },
              { step: "3", title: "Open dashboard", cmd: "http://localhost:3000" },
            ].map((item) => (
              <div key={item.step} className="flex items-start gap-4">
                <div className="w-7 h-7 rounded-full bg-primary/10 text-primary text-sm font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
                  {item.step}
                </div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-foreground mb-1">{item.title}</div>
                  <code className="text-xs bg-muted px-3 py-1.5 rounded-lg text-muted-foreground block font-mono">
                    {item.cmd}
                  </code>
                </div>
                <CheckCircle2 className="w-4 h-4 text-muted-foreground mt-1" />
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="border-t border-border/50 py-8 text-center text-sm text-muted-foreground">
        ATS Resume Optimizer · Local AI · Open Source
      </footer>
    </div>
  );
}
