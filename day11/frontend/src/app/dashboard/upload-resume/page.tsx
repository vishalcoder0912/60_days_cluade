"use client";
import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, FileText, CheckCircle2, Loader2 } from "lucide-react";
import { resumeApi } from "@/lib/api";

export default function UploadResumePage() {
  const [resumes, setResumes] = useState<any[]>([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const onDrop = useCallback(async (accepted: File[]) => {
    if (!accepted.length) return;
    setUploading(true);
    setError("");
    try {
      const results = await Promise.all(accepted.map((f) => resumeApi.upload(f)));
      setResumes((prev) => [...results.map((r) => r.data), ...prev]);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Upload failed");
    } finally {
      setUploading(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
      "text/plain": [".txt"],
    },
    multiple: true,
    disabled: uploading,
  });

  return (
    <div className="max-w-2xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">Upload Resume</h1>
        <p className="text-muted-foreground mt-1 text-sm">
          Supports PDF, DOCX, and TXT. AI will parse and structure your resume automatically.
        </p>
      </div>

      <div {...getRootProps()}
        className={`relative border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all ${
          isDragActive ? "border-primary bg-primary/5" : "border-border hover:border-primary/50 hover:bg-accent/50"
        } ${uploading ? "pointer-events-none opacity-60" : ""}`}>
        <input {...getInputProps()} />
        <div className="flex flex-col items-center gap-4">
          {uploading ? (
            <Loader2 className="w-12 h-12 text-primary animate-spin" />
          ) : (
            <div className="w-14 h-14 rounded-2xl bg-primary/10 flex items-center justify-center">
              <Upload className="w-7 h-7 text-primary" />
            </div>
          )}
          <div>
            <p className="text-base font-medium text-foreground">
              {uploading ? "Uploading & parsing..." : isDragActive ? "Drop here" : "Drop your resume here"}
            </p>
            <p className="text-sm text-muted-foreground mt-1">or click to browse · PDF, DOCX, TXT · max 10MB</p>
          </div>
        </div>
      </div>

      {error && (
        <div className="mt-4 bg-destructive/10 border border-destructive/20 rounded-lg px-4 py-3 text-sm text-destructive">{error}</div>
      )}

      <AnimatePresence>
        {resumes.length > 0 && (
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mt-6 space-y-3">
            <h2 className="text-sm font-semibold text-foreground">Just uploaded</h2>
            {resumes.map((r: any) => (
              <div key={r.id} className="flex items-center gap-4 bg-card border border-border rounded-xl px-5 py-4">
                <div className="w-9 h-9 rounded-lg bg-green-500/10 flex items-center justify-center">
                  <CheckCircle2 className="w-5 h-5 text-green-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-foreground truncate">{r.filename}</div>
                  <div className="text-xs text-muted-foreground">Parsing in background...</div>
                </div>
                <FileText className="w-4 h-4 text-muted-foreground" />
              </div>
            ))}
            <p className="text-xs text-muted-foreground px-1">
              AI is extracting your skills, experience, and education. This takes ~30-60s.
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="mt-8 bg-card border border-border rounded-xl p-5">
        <h3 className="text-sm font-semibold text-foreground mb-3">What happens after upload?</h3>
        <div className="space-y-2">
          {[
            "Text is extracted from your file",
            "AI parses name, contact, skills, experience, education",
            "Embeddings are stored locally in ChromaDB",
            "Resume is ready for ATS scoring and optimization",
          ].map((step, i) => (
            <div key={i} className="flex items-start gap-3 text-sm text-muted-foreground">
              <span className="w-5 h-5 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
                {i + 1}
              </span>
              {step}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
