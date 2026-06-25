import {SectionHeading} from "../components/SectionHeading";
import {SkillPill} from "../components/SkillPill";
import {WobblyCard} from "../components/WobblyCard";
import {skillGroups} from "../data/skills";

export function TechStack() {
  return (
    <section className="container-sketch py-14" id="tech-stack">
      <SectionHeading title="Tech Stack" eyebrow="tools I use" />
      <div className="grid gap-6 lg:grid-cols-3">
        {skillGroups.map((group, index) => (
          <WobblyCard key={group.title} decoration={index === 0 ? "tape" : "none"} tone={index === 1 ? "note" : "white"} className={index % 2 === 0 ? "-rotate-1" : "rotate-1"}>
            <h3 className="font-heading text-3xl leading-none">{group.title}</h3>
            <div className="mt-4 flex flex-wrap gap-2">
              {group.skills.map((skill, skillIndex) => (
                <SkillPill key={skill} tone={skillIndex % 4 === 0 ? "blue" : skillIndex % 5 === 0 ? "red" : "default"}>
                  {skill}
                </SkillPill>
              ))}
            </div>
          </WobblyCard>
        ))}
      </div>
    </section>
  );
}
