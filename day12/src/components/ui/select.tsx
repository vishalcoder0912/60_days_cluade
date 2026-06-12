import { createContext, useContext, forwardRef, useState, type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface SelectContextType {
  value: string;
  onChange: (v: string) => void;
  open: boolean;
  setOpen: (o: boolean) => void;
}
const SelectContext = createContext<SelectContextType>(null!);

function Select({ value, onValueChange, children }: { value: string; onValueChange: (v: string) => void; children: ReactNode }) {
  const [open, setOpen] = useState(false);
  return (
    <SelectContext.Provider value={{ value, onChange: onValueChange, open, setOpen }}>
      <div className="relative">{children}</div>
    </SelectContext.Provider>
  );
}

const SelectTrigger = forwardRef<HTMLButtonElement, { className?: string; children?: ReactNode }>(
  ({ className, children }, ref) => {
    const { setOpen } = useContext(SelectContext);
    return (
      <button
        ref={ref}
        type="button"
        onClick={() => setOpen(true)}
        className={cn(
          "flex h-10 w-full items-center justify-between rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
          className,
        )}
        style={{ colorScheme: "dark" }}
      >
        {children}
        <svg className="size-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
    );
  },
);
SelectTrigger.displayName = "SelectTrigger";

function SelectValue({ placeholder }: { placeholder?: string }) {
  const { value } = useContext(SelectContext);
  return <span>{value || placeholder}</span>;
}

const SelectContent = forwardRef<HTMLDivElement, { className?: string; children?: ReactNode }>(
  ({ className, children }, ref) => {
    const { open, setOpen } = useContext(SelectContext);
    if (!open) return null;
    return (
      <>
        <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
        <div
          ref={ref}
          className={cn(
            "absolute left-0 top-full z-50 mt-1 w-full min-w-[8rem] rounded-lg border border-border bg-popover p-1 shadow-lg",
            className,
          )}
        >
          {children}
        </div>
      </>
    );
  },
);
SelectContent.displayName = "SelectContent";

function SelectItem({ value, children, className }: { value: string; children: ReactNode; className?: string }) {
  const ctx = useContext(SelectContext);
  const selected = ctx.value === value;
  return (
    <div
      role="button"
      tabIndex={0}
      onClick={() => { ctx.onChange(value); ctx.setOpen(false); }}
      className={cn(
        "relative flex w-full cursor-default select-none items-center rounded-md px-2 py-1.5 text-sm outline-none text-foreground hover:bg-secondary",
        selected && "text-primary font-medium",
        className,
      )}
    >
      {children}
    </div>
  );
}

export { Select, SelectContent, SelectItem, SelectTrigger, SelectValue };
