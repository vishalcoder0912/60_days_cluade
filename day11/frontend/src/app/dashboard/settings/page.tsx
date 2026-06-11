"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Settings, User, Shield, Info } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

export default function SettingsPage() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState("profile");

  const tabs = [
    { key: "profile", label: "Profile", icon: User },
    { key: "security", label: "Security", icon: Shield },
    { key: "about", label: "About", icon: Info },
  ];

  return (
    <div className="max-w-2xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">Settings</h1>
        <p className="text-muted-foreground mt-1 text-sm">Manage your account and preferences.</p>
      </div>

      <div className="flex gap-1 bg-card border border-border rounded-xl p-1 mb-6 w-fit">
        {tabs.map((t) => (
          <button key={t.key} onClick={() => setActiveTab(t.key)}
            className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              activeTab === t.key ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground"
            }`}>
            <t.icon className="w-3.5 h-3.5" />
            {t.label}
          </button>
        ))}
      </div>

      <motion.div key={activeTab} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
        {activeTab === "profile" && (
          <div className="bg-card border border-border rounded-2xl p-6">
            <h2 className="text-sm font-semibold text-foreground mb-4">Profile Information</h2>
            <div className="space-y-4">
              <div>
                <label className="text-sm text-muted-foreground block mb-1">Name</label>
                <div className="text-sm text-foreground bg-background border border-border rounded-lg px-3 py-2.5">
                  {user?.name || "-"}
                </div>
              </div>
              <div>
                <label className="text-sm text-muted-foreground block mb-1">Email</label>
                <div className="text-sm text-foreground bg-background border border-border rounded-lg px-3 py-2.5">
                  {user?.email || "-"}
                </div>
              </div>
              <div>
                <label className="text-sm text-muted-foreground block mb-1">User ID</label>
                <div className="text-sm text-muted-foreground bg-background border border-border rounded-lg px-3 py-2.5 font-mono">
                  {user?.id || "-"}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "security" && (
          <div className="bg-card border border-border rounded-2xl p-6">
            <h2 className="text-sm font-semibold text-foreground mb-4">Security</h2>
            <div className="space-y-3">
              <div className="bg-background border border-border rounded-xl p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm font-medium text-foreground">Authentication</div>
                    <div className="text-xs text-muted-foreground mt-0.5">Disabled for local demo mode</div>
                  </div>
                  <Shield className="w-4 h-4 text-green-400" />
                </div>
              </div>
              <div className="bg-background border border-border rounded-xl p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm font-medium text-foreground">Token</div>
                    <div className="text-xs text-muted-foreground mt-0.5">No browser token required</div>
                  </div>
                  <Shield className="w-4 h-4 text-green-400" />
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "about" && (
          <div className="bg-card border border-border rounded-2xl p-6">
            <h2 className="text-sm font-semibold text-foreground mb-4">About</h2>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Version</span>
                <span className="text-foreground">1.0.0</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">AI Backend</span>
                <span className="text-foreground">OpenRouter (Google Gemma 4 - Free)</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Database</span>
                <span className="text-foreground">SQLite</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Framework</span>
                <span className="text-foreground">FastAPI + Next.js 15</span>
              </div>
              <div className="border-t border-border pt-3 mt-3">
                <p className="text-xs text-muted-foreground">
                  Free AI powered by OpenRouter. No paid API keys required.
                </p>
              </div>
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
}
