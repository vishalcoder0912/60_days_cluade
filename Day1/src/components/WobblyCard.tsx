import type {HTMLAttributes, ReactNode} from "react";

type WobblyCardProps = HTMLAttributes<HTMLElement> & {
  children: ReactNode;
  as?: "article" | "div" | "section";
  decoration?: "tape" | "tack" | "none";
  tone?: "white" | "note" | "muted";
};

export function WobblyCard({
  children,
  as: Component = "article",
  decoration = "none",
  tone = "white",
  className = "",
  ...props
}: WobblyCardProps) {
  const toneClass = {
    white: "bg-white",
    note: "bg-note",
    muted: "bg-muted",
  }[tone];

  return (
    <Component
      className={`relative rounded-wobblyMd border-[3px] border-ink ${toneClass} p-5 shadow-paper transition duration-100 hover:-translate-y-0.5 hover:rotate-0 hover:shadow-[6px_6px_0_0_rgba(45,45,45,0.24)] ${className}`}
      {...props}
    >
      {decoration === "tape" ? (
        <span className="absolute left-1/2 top-0 h-8 w-28 -translate-x-1/2 -translate-y-4 rotate-2 border-x-2 border-dashed border-ink/25 bg-muted/80" aria-hidden="true" />
      ) : null}
      {decoration === "tack" ? (
        <span className="absolute left-1/2 top-0 h-5 w-5 -translate-x-1/2 -translate-y-3 rounded-[999px_860px_930px_780px/820px_900px_760px_920px] border-2 border-ink bg-marker shadow-[2px_2px_0_0_#2d2d2d]" aria-hidden="true" />
      ) : null}
      {children}
    </Component>
  );
}
