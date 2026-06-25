import {GraduationCap} from "lucide-react";
import {SectionHeading} from "../components/SectionHeading";
import {WobblyCard} from "../components/WobblyCard";

export function Education() {
  return (
    <section className="container-sketch py-14" id="education">
      <SectionHeading title="Education" eyebrow="completed" />
      <WobblyCard decoration="tape" tone="note" className="rotate-1">
        <div className="flex flex-col gap-5 sm:flex-row sm:items-start">
          <span className="inline-flex h-14 w-14 shrink-0 items-center justify-center rounded-[49%_51%_44%_56%/56%_42%_58%_44%] border-2 border-ink bg-white text-pen shadow-[3px_3px_0_0_#2d2d2d]">
            <GraduationCap size={32} strokeWidth={2.8} />
          </span>
          <div>
            <h3 className="font-heading text-4xl leading-none">Bachelor of Computer Applications</h3>
            <p className="mt-2 text-2xl leading-snug">IMS Noida, Computer Science</p>
            <p className="mt-2 text-2xl leading-snug">Graduation completed in 2026.</p>
            <p className="mt-4 border-t-2 border-dashed border-ink/40 pt-4 text-xl leading-snug">
              Project-driven learning approach with strong practical focus across MERN development, AI workflows, dashboards, and product-oriented frontend work.
            </p>
          </div>
        </div>
      </WobblyCard>
    </section>
  );
}
