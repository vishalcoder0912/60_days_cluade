import { FileText, Sparkles, Upload } from "lucide-react";
import { useRef, useState, type FormEvent } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { fileToBase64 } from "@/lib/run-careerforge";
import type { CareerInput, Experience } from "@/lib/types";

const EXPERIENCES: Experience[] = [
  "Intern",
  "Entry",
  "Mid",
  "Senior",
  "Lead",
  "Executive",
];

export function InputForm({
  onSubmit,
  loading,
}: {
  onSubmit: (input: CareerInput) => void;
  loading: boolean;
}) {
  const [role, setRole] = useState("");
  const [company, setCompany] = useState("");
  const [location, setLocation] = useState("");
  const [experience, setExperience] = useState<Experience>("Mid");
  const [jobDescription, setJobDescription] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);
  const roleRef = useRef<HTMLInputElement>(null);
  const companyRef = useRef<HTMLInputElement>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const roleVal = (roleRef.current?.value || role).trim();
    const companyVal = (companyRef.current?.value || company).trim();
    if (!roleVal || !companyVal) {
      toast.error("Please enter a target role and company.");
      return;
    }
    if (!file && resumeText.trim().length < 40) {
      toast.error("Upload a resume file or paste your resume text.");
      return;
    }

    const input: CareerInput = {
      role: roleVal,
      company: companyVal,
      location: location.trim() || undefined,
      experience,
      jobDescription: jobDescription.trim() || undefined,
    };

    if (file) {
      if (file.type === "text/plain") {
        input.resumeText = await file.text();
      } else {
        input.resumeFile = {
          name: file.name,
          mime: file.type || "application/octet-stream",
          dataBase64: await fileToBase64(file),
        };
      }
    } else {
      input.resumeText = resumeText.trim();
    }
    onSubmit(input);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="glass mx-auto w-full max-w-3xl rounded-2xl p-6 shadow-elegant sm:p-8"
    >
      <div className="grid gap-5 sm:grid-cols-2">
        <div className="space-y-2">
          <Label htmlFor="role">Target job role *</Label>
          <Input
            ref={roleRef}
            id="role"
            placeholder="Frontend Developer"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="company">Company *</Label>
          <Input
            ref={companyRef}
            id="company"
            placeholder="Google"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="location">Preferred location</Label>
          <Input
            id="location"
            placeholder="Bangalore"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
        </div>
        <div className="space-y-2">
          <Label>Experience level</Label>
          <Select
            value={experience}
            onValueChange={(v) => setExperience(v as Experience)}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {EXPERIENCES.map((x) => (
                <SelectItem key={x} value={x}>
                  {x}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="mt-5 space-y-2">
        <Label>Resume *</Label>
        <button
          type="button"
          onClick={() => fileRef.current?.click()}
          className="flex w-full items-center gap-3 rounded-xl border border-dashed border-border bg-background/40 px-4 py-5 text-left transition-colors hover:border-primary/60"
        >
          <span className="grid size-10 place-items-center rounded-lg gradient-primary text-primary-foreground">
            {file ? <FileText className="size-5" /> : <Upload className="size-5" />}
          </span>
          <span className="text-sm">
            <span className="block font-medium text-foreground">
              {file ? file.name : "Upload resume (PDF, DOCX, or TXT)"}
            </span>
            <span className="text-muted-foreground">
              {file ? "Click to replace" : "Click to browse — or paste text below"}
            </span>
          </span>
        </button>
        <input
          ref={fileRef}
          type="file"
          accept=".pdf,.doc,.docx,.txt"
          className="hidden"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <Textarea
          placeholder="…or paste your full resume text here"
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
          rows={4}
          disabled={!!file}
          className="mt-2"
        />
      </div>

      <div className="mt-5 space-y-2">
        <Label htmlFor="jd">Job description (optional)</Label>
        <Textarea
          id="jd"
          placeholder="Paste the job posting for sharper, tailored results"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          rows={4}
        />
      </div>

      <Button
        type="submit"
        size="lg"
        disabled={loading}
        className="mt-6 w-full gradient-primary text-primary-foreground shadow-glow"
      >
        <Sparkles className="size-5" />
        {loading ? "Forging your toolkit…" : "Generate my career toolkit"}
      </Button>
    </form>
  );
}
