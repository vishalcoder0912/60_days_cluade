import type {LucideIcon} from "lucide-react";

type ContactLinkProps = {
  href: string;
  icon: LucideIcon;
  title: string;
  label: string;
};

export function ContactLink({href, icon: Icon, title, label}: ContactLinkProps) {
  return (
    <a
      className="group rounded-wobblyMd border-[3px] border-ink bg-white p-5 text-ink shadow-hard transition duration-100 hover:translate-x-0.5 hover:translate-y-0.5 hover:bg-note hover:shadow-[2px_2px_0_0_#2d2d2d]"
      href={href}
    >
      <span className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-[49%_51%_44%_56%/56%_42%_58%_44%] border-2 border-ink bg-paper text-pen group-hover:text-marker">
        <Icon size={25} strokeWidth={2.8} />
      </span>
      <strong className="block font-heading text-3xl leading-none">{title}</strong>
      <span className="mt-2 block [overflow-wrap:anywhere] text-xl leading-tight">{label}</span>
    </a>
  );
}
