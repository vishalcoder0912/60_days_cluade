import { useState } from "react";
import {
  FileSearch,
  Linkedin,
  MessageSquare,
  Search,
  Sparkles,
  Target,
} from "lucide-react";
import { toast } from "sonner";
import { Dashboard } from "@/components/careerforge/Dashboard";
import { InputForm } from "@/components/careerforge/InputForm";
import { RunningView } from "@/components/careerforge/RunningView";
import { runCareerForge } from "@/lib/run-careerforge";
import type { CareerInput, CareerReport } from "@/lib/types";

type Phase =
  | { kind: "input" }
  | { kind: "running"; step: number }
  | { kind: "done"; report: CareerReport };

const FEATURES = [
  { icon: FileSearch, label: "Resume & ATS analysis" },
  { icon: Search, label: "Live company research" },
  { icon: Target, label: "Skill-gap roadmap" },
  { icon: Sparkles, label: "Interview & cover letters" },
  { icon: Linkedin, label: "LinkedIn optimizer" },
  { icon: MessageSquare, label: "Outreach templates" },
];

export default function Index() {
  const [phase, setPhase] = useState<Phase>({ kind: "input" });

  async function handleSubmit(input: CareerInput) {
    setPhase({ kind: "running", step: 0 });
    try {
      const report = await runCareerForge(input, (step) =>
        setPhase({ kind: "running", step }),
      );
      setPhase({ kind: "done", report });
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Something went wrong.";
      toast.error(msg);
      setPhase({ kind: "input" });
    }
  }

  return (
    <main className="hero-bg min-h-screen px-4 py-10 sm:py-16">
      {phase.kind === "done" ? (
        <Dashboard
          report={phase.report}
          onReset={() => setPhase({ kind: "input" })}
        />
      ) : (
        <div className="mx-auto w-full max-w-3xl">
          <header className="mb-8 text-center">
            <span className="glass inline-flex items-center gap-2 rounded-full px-4 py-1.5 text-xs font-medium text-muted-foreground">
              <Sparkles className="size-3.5 text-primary" /> AI-Powered Job Search Toolkit
            </span>
            <h1 className="mt-4 text-4xl font-extrabold tracking-tight sm:text-5xl">
              <span className="gradient-text">CareerForge AI</span>
            </h1>
            <p className="mx-auto mt-3 max-w-xl text-balance text-muted-foreground">
              Upload your resume and target a role — get a complete, downloadable
              application toolkit: ATS analysis, live company research, interview prep,
              cover letters, LinkedIn copy, and outreach messages.
            </p>
            <div className="mt-6 flex flex-wrap justify-center gap-2">
              {FEATURES.map((f) => (
                <span
                  key={f.label}
                  className="glass inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs text-muted-foreground"
                >
                  <f.icon className="size-3.5 text-accent" />
                  {f.label}
                </span>
              ))}
            </div>
          </header>
          {phase.kind === "running" ? (
            <RunningView current={phase.step} />
          ) : (
            <InputForm onSubmit={handleSubmit} loading={false} />
          )}
        </div>
      )}
    </main>
  );
}
