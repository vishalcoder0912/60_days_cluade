import {ExternalLink, Github} from "lucide-react";
import type {Project} from "../data/projects";
import {SkillPill} from "./SkillPill";
import {WobblyCard} from "./WobblyCard";

type ProjectCardProps = {
  project: Project;
  index: number;
};

export function ProjectCard({project, index}: ProjectCardProps) {
  return (
    <WobblyCard
      decoration={index % 2 === 0 ? "tack" : "tape"}
      tone={index === 0 ? "note" : "white"}
      className={`${index % 2 === 0 ? "-rotate-1" : "rotate-1"} flex h-full flex-col gap-4`}
    >
      <div>
        <span className="inline-flex rounded-wobbly border-2 border-ink bg-muted px-3 py-1 text-lg font-bold leading-none text-pen">
          {project.label}
        </span>
        <h3 className="mt-4 font-heading text-3xl leading-none">{project.name}</h3>
        {project.highlight ? <p className="mt-2 text-xl font-bold text-marker">{project.highlight}</p> : null}
      </div>
      <p className="text-xl leading-snug">{project.description}</p>
      <div className="flex flex-wrap gap-2">
        {project.tags.map((tag, tagIndex) => (
          <SkillPill key={tag} tone={tagIndex % 5 === 0 ? "blue" : tagIndex % 4 === 0 ? "red" : "default"}>
            {tag}
          </SkillPill>
        ))}
      </div>
      <div className="mt-auto flex flex-wrap gap-3 pt-2">
        <a className="inline-flex items-center gap-2 rounded-wobbly border-2 border-ink bg-white px-3 py-2 text-xl leading-none shadow-[3px_3px_0_0_#2d2d2d] transition duration-100 hover:bg-marker hover:text-white hover:shadow-[1px_1px_0_0_#2d2d2d]" href={project.github}>
          <Github size={20} strokeWidth={2.8} />
          GitHub
        </a>
        {project.links?.map((link) => (
          <a key={link.href} className="inline-flex items-center gap-2 rounded-wobbly border-2 border-ink bg-muted px-3 py-2 text-xl leading-none transition duration-100 hover:bg-pen hover:text-white" href={link.href}>
            <ExternalLink size={18} strokeWidth={2.8} />
            {link.label}
          </a>
        ))}
      </div>
    </WobblyCard>
  );
}
