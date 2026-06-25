import type {AnchorHTMLAttributes, ReactNode} from "react";

type ButtonProps = AnchorHTMLAttributes<HTMLAnchorElement> & {
  children: ReactNode;
  variant?: "primary" | "secondary";
};

export function Button({children, variant = "primary", className = "", ...props}: ButtonProps) {
  const variantClass =
    variant === "primary"
      ? "bg-white hover:bg-marker hover:text-white"
      : "bg-muted hover:bg-pen hover:text-white";

  return (
    <a
      className={`inline-flex min-h-12 items-center justify-center rounded-wobbly border-[3px] border-ink px-5 py-2 font-body text-2xl leading-none text-ink shadow-hard transition duration-100 hover:translate-x-0.5 hover:translate-y-0.5 hover:shadow-[2px_2px_0_0_#2d2d2d] active:translate-x-1 active:translate-y-1 active:shadow-none ${variantClass} ${className}`}
      {...props}
    >
      {children}
    </a>
  );
}
