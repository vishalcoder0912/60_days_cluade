import {BriefcaseBusiness} from "lucide-react";
import {Button} from "../components/Button";

const links = [
  {label: "Proof", href: "#github-proof"},
  {label: "Projects", href: "#projects"},
  {label: "Experience", href: "#experience"},
  {label: "Contact", href: "#contact"},
];

export function Nav() {
  return (
    <header className="sticky top-0 z-50 border-b-[3px] border-dashed border-ink/30 bg-paper/92 backdrop-blur-sm">
      <nav className="container-sketch flex min-h-20 items-center justify-between gap-4 py-3" aria-label="Primary navigation">
        <a className="flex items-center gap-3 font-heading text-2xl leading-none text-pen" href="#top">
          <span className="flex h-11 w-11 rotate-[-2deg] items-center justify-center rounded-[49%_51%_44%_56%/56%_42%_58%_44%] border-2 border-ink bg-note shadow-[3px_3px_0_0_#2d2d2d]">
            <BriefcaseBusiness size={22} strokeWidth={2.8} />
          </span>
          Open To Work
        </a>
        <div className="hidden items-center gap-5 md:flex">
          {links.map((link) => (
            <a key={link.href} className="text-xl leading-none transition hover:text-marker hover:line-through" href={link.href}>
              {link.label}
            </a>
          ))}
        </div>
        <Button className="hidden md:inline-flex" href="#contact">
          Hire / Collaborate
        </Button>
      </nav>
    </header>
  );
}
