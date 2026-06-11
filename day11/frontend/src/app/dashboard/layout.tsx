"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import {
  LayoutDashboard, Upload, Briefcase, Zap, FileText,
  Mail, Linkedin, MessageSquare, History, Settings, ShieldOff
} from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

const nav = [
  { href: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { href: "/dashboard/upload-resume", icon: Upload, label: "Upload Resume" },
  { href: "/dashboard/job-analysis", icon: Briefcase, label: "Job Analysis" },
  { href: "/dashboard/ats-score", icon: Zap, label: "ATS Score" },
  { href: "/dashboard/cover-letter", icon: FileText, label: "Cover Letter" },
  { href: "/dashboard/cold-email", icon: Mail, label: "Cold Email" },
  { href: "/dashboard/linkedin", icon: Linkedin, label: "LinkedIn" },
  { href: "/dashboard/interview-prep", icon: MessageSquare, label: "Interview Prep" },
  { href: "/dashboard/history", icon: History, label: "History" },
  { href: "/dashboard/settings", icon: Settings, label: "Settings" },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  const pathname = usePathname();

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      <aside className="w-56 flex-shrink-0 border-r border-border bg-card flex flex-col">
        <div className="px-4 py-4 border-b border-border">
          <Link href="/dashboard" className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-primary flex items-center justify-center">
              <Zap className="w-4 h-4 text-primary-foreground" />
            </div>
            <span className="font-semibold text-sm text-foreground">ATS Optimizer</span>
          </Link>
        </div>
        <nav className="flex-1 px-2 py-3 space-y-0.5 overflow-y-auto">
          {nav.map((item) => {
            const active = pathname === item.href;
            return (
              <Link key={item.href} href={item.href}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                  active
                    ? "bg-primary/10 text-primary font-medium"
                    : "text-muted-foreground hover:text-foreground hover:bg-accent"
                }`}>
                <item.icon className="w-4 h-4 flex-shrink-0" />
                {item.label}
              </Link>
            );
          })}
        </nav>
        <div className="px-3 py-3 border-t border-border">
          <div className="flex items-center gap-3 px-2 py-1.5 mb-1">
            <div className="w-7 h-7 rounded-full bg-primary/20 flex items-center justify-center text-xs font-bold text-primary">
              {user?.name?.[0]?.toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-xs font-medium text-foreground truncate">{user?.name}</div>
              <div className="text-xs text-muted-foreground truncate">{user?.email}</div>
            </div>
          </div>
          <div className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-muted-foreground">
            <ShieldOff className="w-4 h-4" />
            Local mode
          </div>
        </div>
      </aside>
      <main className="flex-1 overflow-y-auto">
        <motion.div key={pathname} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }} className="p-8">
          {children}
        </motion.div>
      </main>
    </div>
  );
}
