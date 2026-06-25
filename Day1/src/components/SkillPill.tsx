type SkillPillProps = {
  children: string;
  tone?: "default" | "blue" | "red";
};

export function SkillPill({children, tone = "default"}: SkillPillProps) {
  const toneClass = {
    default: "text-ink",
    blue: "text-pen",
    red: "text-marker",
  }[tone];

  return (
    <span className={`inline-flex rounded-wobbly border-2 border-ink bg-paper px-3 py-1 text-lg font-bold leading-none ${toneClass}`}>
      {children}
    </span>
  );
}
