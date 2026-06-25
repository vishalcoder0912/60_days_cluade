type StatBadgeProps = {
  value: string;
  label: string;
};

export function StatBadge({value, label}: StatBadgeProps) {
  return (
    <div className="flex min-h-32 flex-col items-center justify-center rounded-[49%_51%_44%_56%/56%_42%_58%_44%] border-[3px] border-ink bg-white p-5 text-center shadow-hard">
      <strong className="font-heading text-3xl leading-none text-pen">{value}</strong>
      <span className="mt-2 max-w-36 text-xl leading-tight">{label}</span>
    </div>
  );
}
