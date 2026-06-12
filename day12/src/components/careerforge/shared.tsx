import { Check, Copy } from "lucide-react";
import { useState, type ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function CopyButton({ text, label = "Copy" }: { text: string; label?: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <Button
      type="button"
      variant="secondary"
      size="sm"
      onClick={() => {
        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 1500);
      }}
    >
      {copied ? <Check className="size-4" /> : <Copy className="size-4" />}
      {copied ? "Copied" : label}
    </Button>
  );
}

export function ScoreRing({
  value,
  size = 132,
  label,
}: {
  value: number;
  size?: number;
  label: string;
}) {
  const stroke = 12;
  const r = (size - stroke) / 2;
  const circ = 2 * Math.PI * r;
  const pct = Math.max(0, Math.min(100, value));
  const offset = circ - (pct / 100) * circ;
  const color =
    pct >= 75 ? "var(--success)" : pct >= 50 ? "var(--warning)" : "var(--destructive)";
  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={r}
            fill="none"
            stroke="var(--muted)"
            strokeWidth={stroke}
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={r}
            fill="none"
            stroke={color}
            strokeWidth={stroke}
            strokeDasharray={circ}
            strokeDashoffset={offset}
            strokeLinecap="round"
            style={{ transition: "stroke-dashoffset 1s ease" }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-3xl font-bold">{pct}</span>
          <span className="text-xs text-muted-foreground">/ 100</span>
        </div>
      </div>
      <span className="text-sm font-medium text-muted-foreground">{label}</span>
    </div>
  );
}

export function Pills({
  items,
  tone = "default",
}: {
  items: string[];
  tone?: "default" | "success" | "danger" | "accent";
}) {
  const toneCls = {
    default: "bg-secondary text-secondary-foreground",
    success: "bg-success/15 text-success border border-success/30",
    danger: "bg-destructive/15 text-destructive border border-destructive/30",
    accent: "bg-accent/15 text-accent border border-accent/30",
  }[tone];
  if (!items.length)
    return <p className="text-sm text-muted-foreground">None listed.</p>;
  return (
    <div className="flex flex-wrap gap-2">
      {items.map((i) => (
        <span key={i} className={cn("rounded-full px-3 py-1 text-xs font-medium", toneCls)}>
          {i}
        </span>
      ))}
    </div>
  );
}

export function Field({
  title,
  children,
  copy,
}: {
  title: string;
  children: ReactNode;
  copy?: string;
}) {
  return (
    <div className="rounded-xl border border-border bg-background/40 p-4">
      <div className="mb-2 flex items-center justify-between gap-2">
        <h4 className="text-sm font-semibold text-foreground">{title}</h4>
        {copy ? <CopyButton text={copy} /> : null}
      </div>
      <div className="text-sm leading-relaxed text-muted-foreground">{children}</div>
    </div>
  );
}
