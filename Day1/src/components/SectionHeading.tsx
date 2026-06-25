type SectionHeadingProps = {
  eyebrow?: string;
  title: string;
  align?: "left" | "center";
};

export function SectionHeading({eyebrow, title, align = "left"}: SectionHeadingProps) {
  return (
    <div className={`mb-8 flex flex-wrap items-end gap-4 ${align === "center" ? "justify-center text-center" : ""}`}>
      <h2 className="font-heading text-4xl leading-none text-ink sm:text-5xl">{title}</h2>
      {eyebrow ? (
        <span className="-rotate-2 rounded-[18px_8px_16px_10px/10px_18px_8px_16px] border-2 border-ink bg-note px-3 py-1 font-body text-xl leading-none shadow-[3px_3px_0_0_#2d2d2d]">
          {eyebrow}
        </span>
      ) : null}
    </div>
  );
}
