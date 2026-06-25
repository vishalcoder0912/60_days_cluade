import {CalendarCheck, Sparkles} from "lucide-react";
import {SectionHeading} from "../components/SectionHeading";
import {WobblyCard} from "../components/WobblyCard";

export function Experience() {
  return (
    <section className="container-sketch py-14" id="experience">
      <SectionHeading title="Experience" eyebrow="internship completed" />
      <WobblyCard decoration="tack" tone="white" className="-rotate-1">
        <div className="grid gap-6 md:grid-cols-[0.8fr_1.2fr] md:items-start">
          <div>
            <div className="mb-4 inline-flex h-14 w-14 items-center justify-center rounded-[49%_51%_44%_56%/56%_42%_58%_44%] border-2 border-ink bg-note text-marker shadow-[3px_3px_0_0_#2d2d2d]">
              <CalendarCheck size={30} strokeWidth={2.8} />
            </div>
            <h3 className="font-heading text-4xl leading-none">Web Developer at NoirSane</h3>
            <p className="mt-2 text-2xl text-pen">Completed 10-month Web Developer internship</p>
          </div>
          <div className="space-y-3 text-2xl leading-snug">
            <p>
              Worked on React, Firebase, responsive UI, payment flows, landing pages, and user experience improvements.
            </p>
            <p className="flex gap-3 rounded-wobbly border-2 border-dashed border-ink bg-paper p-4 text-xl">
              <Sparkles className="mt-1 shrink-0 text-marker" size={24} strokeWidth={2.8} />
              Practical work included modern web interfaces, product presentation, frontend polish, Firebase integrations, and performance-minded responsive layouts.
            </p>
          </div>
        </div>
      </WobblyCard>
    </section>
  );
}
