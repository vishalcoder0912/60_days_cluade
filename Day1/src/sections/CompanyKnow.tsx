import {WobblyCard} from "../components/WobblyCard";
import {companyNotes} from "../data/profile";

export function CompanyKnow() {
  return (
    <section className="container-sketch py-14" id="company-notes">
      <WobblyCard decoration="tack" tone="white">
        <div className="grid gap-4 md:grid-cols-5">
          {companyNotes.map((note, index) => (
            <div key={note} className="rounded-wobbly border-2 border-dashed border-ink bg-paper p-4 text-center">
              <strong className="block font-heading text-3xl leading-none text-marker">{String(index + 1).padStart(2, "0")}</strong>
              <span className="mt-2 block text-xl leading-tight">{note}</span>
            </div>
          ))}
        </div>
      </WobblyCard>
    </section>
  );
}
