import { createContext, useContext, useState, type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface ItemContextType {
  value: string;
}
const ItemContext = createContext<ItemContextType>({ value: "" });

interface AccordionContextType {
  openValue: string | null;
  setOpen: (v: string | null) => void;
}
const AccordionContext = createContext<AccordionContextType>(null!);

function Accordion({ type = "single", collapsible = true, className, children }: {
  type?: "single" | "multiple";
  collapsible?: boolean;
  className?: string;
  children: ReactNode;
}) {
  const [openValue, setOpen] = useState<string | null>(null);
  return (
    <AccordionContext.Provider value={{ openValue, setOpen }}>
      <div className={cn("space-y-1", className)}>{children}</div>
    </AccordionContext.Provider>
  );
}

function AccordionItem({ value, className, children }: { value: string; className?: string; children: ReactNode }) {
  const ctx = useContext(AccordionContext);
  const isOpen = ctx.openValue === value;
  return (
    <ItemContext.Provider value={{ value }}>
      <div className={cn("border-b border-border", isOpen && "pb-2", className)}>
        {children}
      </div>
    </ItemContext.Provider>
  );
}

function AccordionTrigger({ className, children }: { className?: string; children: ReactNode }) {
  const aCtx = useContext(AccordionContext);
  const iCtx = useContext(ItemContext);
  const isOpen = aCtx.openValue === iCtx.value;
  return (
    <h3>
      <button
        type="button"
        data-state={isOpen ? "open" : "closed"}
        className={cn(
          "flex w-full items-center justify-between py-4 text-sm font-medium transition-all hover:underline",
          className,
        )}
        onClick={() => aCtx.setOpen(isOpen ? null : iCtx.value)}
      >
        {children}
        <svg
          className={cn("size-4 shrink-0 transition-transform duration-200", isOpen && "rotate-180")}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
    </h3>
  );
}

function AccordionContent({ className, children }: { className?: string; children: ReactNode }) {
  const aCtx = useContext(AccordionContext);
  const iCtx = useContext(ItemContext);
  const isOpen = aCtx.openValue === iCtx.value;
  if (!isOpen) return null;
  return <div className={cn("pb-4 pt-0 text-sm", className)}>{children}</div>;
}

export { Accordion, AccordionContent, AccordionItem, AccordionTrigger };
