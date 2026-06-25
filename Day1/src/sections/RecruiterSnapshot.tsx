import {SectionHeading} from "../components/SectionHeading";
import {WobblyCard} from "../components/WobblyCard";
import {snapshot} from "../data/profile";

export function RecruiterSnapshot() {
  return (
    <section className="container-sketch py-14" id="snapshot">
      <SectionHeading title="Recruiter Snapshot" eyebrow="quick read" />
      <div className="grid gap-6 md:grid-cols-3">
        {snapshot.map((block, index) => (
          <WobblyCard key={block.title} decoration={index === 1 ? "tape" : "tack"} tone={index === 1 ? "note" : "white"} className={index % 2 === 0 ? "-rotate-1" : "rotate-1"}>
            <h3 className="font-heading text-3xl leading-none">{block.title}</h3>
            <ul className="mt-4 space-y-2 text-xl leading-snug">
              {block.items.map((item) => (
                <li key={item} className="relative pl-5 before:absolute before:left-0 before:top-0 before:font-heading before:text-marker before:content-['>']">
                  {item}
                </li>
              ))}
            </ul>
          </WobblyCard>
        ))}
      </div>
    </section>
  );
}
