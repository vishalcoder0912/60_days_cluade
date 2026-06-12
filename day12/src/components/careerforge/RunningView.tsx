import { Check, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { STEPS } from "@/lib/run-careerforge";

export function RunningView({ current }: { current: number }) {
  return (
    <div className="glass mx-auto w-full max-w-lg rounded-2xl p-8">
      <h2 className="mb-1 text-center text-lg font-semibold">Forging your toolkit</h2>
      <p className="mb-6 text-center text-sm text-muted-foreground">
        Running live research and AI analysis — this takes a minute.
      </p>
      <ol className="space-y-3">
        {STEPS.map((step, i) => {
          const done = i < current;
          const active = i === current;
          return (
            <li
              key={step}
              className={cn(
                "flex items-center gap-3 rounded-xl border px-4 py-3 transition-colors",
                active ? "border-primary/50 bg-primary/10" : "border-border",
              )}
            >
              <span
                className={cn(
                  "grid size-7 shrink-0 place-items-center rounded-full text-xs",
                  done && "bg-success text-background",
                  active && "gradient-primary text-primary-foreground",
                  !done && !active && "bg-muted text-muted-foreground",
                )}
              >
                {done ? (
                  <Check className="size-4" />
                ) : active ? (
                  <Loader2 className="size-4 animate-spin" />
                ) : (
                  i + 1
                )}
              </span>
              <span
                className={cn(
                  "text-sm",
                  active ? "font-medium text-foreground" : "text-muted-foreground",
                )}
              >
                {step}
              </span>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
