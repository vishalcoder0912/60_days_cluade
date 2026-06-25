import {Github, Linkedin, Mail} from "lucide-react";
import {Button} from "../components/Button";
import {ContactLink} from "../components/ContactLink";
import {SectionHeading} from "../components/SectionHeading";
import {profile} from "../data/profile";

export function Contact() {
  return (
    <footer className="container-sketch pb-12 pt-14" id="contact">
      <SectionHeading title="Hire / Collaborate" eyebrow="contact footer" />
      <div className="grid gap-5 lg:grid-cols-3">
        <ContactLink href={`mailto:${profile.email}`} icon={Mail} title="Email" label={profile.email} />
        <ContactLink href={profile.github} icon={Github} title="GitHub" label={profile.githubLabel} />
        <ContactLink href={profile.linkedin} icon={Linkedin} title="LinkedIn" label={profile.linkedinLabel} />
      </div>
      <div className="mt-8 flex flex-wrap gap-4">
        <Button href={`mailto:${profile.email}`}>Email Me</Button>
        <Button href={profile.github} variant="secondary">
          View GitHub
        </Button>
        <Button href={profile.linkedin} variant="secondary">
          Open LinkedIn
        </Button>
      </div>
      <p className="mt-10 border-t-[3px] border-dashed border-ink/35 pt-5 text-xl">
        {profile.name} / {profile.role} / {profile.status}
      </p>
    </footer>
  );
}
