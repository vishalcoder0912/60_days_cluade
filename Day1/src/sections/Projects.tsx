import {SectionHeading} from "../components/SectionHeading";
import {ProjectCard} from "../components/ProjectCard";
import {projects} from "../data/projects";

export function Projects() {
  return (
    <section className="container-sketch py-14" id="projects">
      <SectionHeading title="Featured Projects" eyebrow="selected proof" />
      <div className="grid gap-6 lg:grid-cols-2">
        {projects.map((project, index) => (
          <ProjectCard key={project.name} project={project} index={index} />
        ))}
      </div>
    </section>
  );
}
