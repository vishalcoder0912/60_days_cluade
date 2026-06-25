import {Github} from "lucide-react";
import {SectionHeading} from "../components/SectionHeading";
import {StatBadge} from "../components/StatBadge";
import {WobblyCard} from "../components/WobblyCard";
import {githubProof} from "../data/stats";

export function GitHubProof() {
  return (
    <section className="container-sketch py-14" id="github-proof">
      <SectionHeading title="GitHub Proof" eyebrow="activity, not fluff" />
      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="grid gap-5 sm:grid-cols-2">
          {githubProof.map((stat) => (
            <StatBadge key={stat.label} {...stat} />
          ))}
        </div>
        <WobblyCard decoration="tape" tone="note" className="rotate-1">
          <div className="mb-5 inline-flex h-14 w-14 items-center justify-center rounded-[49%_51%_44%_56%/56%_42%_58%_44%] border-2 border-ink bg-white text-pen shadow-[3px_3px_0_0_#2d2d2d]">
            <Github size={30} strokeWidth={2.8} />
          </div>
          <h3 className="font-heading text-4xl leading-none">Current daily repo: freelance</h3>
          <p className="mt-4 text-2xl leading-snug">
            Currently building daily in <strong>freelance</strong>, a multi-project repository focused on school management modules, interactive learning dashboards, UI improvements, child-friendly games, progress tracking, and production-style frontend structure.
          </p>
          <p className="mt-4 border-t-2 border-dashed border-ink/40 pt-4 text-xl leading-snug">
            Recent work includes school management modules, interactive games, progress tracking, localStorage persistence, educational dashboards, and UI improvements.
          </p>
        </WobblyCard>
      </div>
    </section>
  );
}
