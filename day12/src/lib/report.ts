import type { CareerReport } from "./types";

function list(items: string[], bullet = "-"): string {
  return items.length ? items.map((i) => `${bullet} ${i}`).join("\n") : "_None_";
}

export function buildMarkdown(r: CareerReport): string {
  const a = r.analysis;
  const c = r.research.company;
  const role = r.research.role;
  const s = r.strategy;
  const iv = r.interview;
  const b = r.branding;

  return `# CareerForge AI — Job Application Toolkit
**Candidate:** ${a.candidateName}
**Target Role:** ${r.input.role}
**Company:** ${r.input.company}${r.input.location ? `\n**Location:** ${r.input.location}` : ""}
**Experience:** ${r.input.experience}
**Generated:** ${new Date(r.generatedAt).toLocaleString()}
---
## 1. Resume Improvement & ATS Report
- **ATS Score:** ${a.atsScore}/100
- **Resume Health:** ${a.resumeHealth}/100
### Strengths
${list(a.strengths)}
### Weaknesses
${list(a.weaknesses)}
### Missing Keywords
${list(a.missingKeywords)}
### Missing Technical Skills
${list(a.missingSkills)}
### Improvement Suggestions
${list(a.suggestions)}
### Extracted Skills
${list(a.skills)}
---
## 2. Company Intelligence Report — ${r.input.company}
**Overview:** ${c.overview}
**Mission:** ${c.mission}
### Values
${list(c.values)}
### Recent News
${list(c.recentNews)}
### Product Launches
${list(c.productLaunches)}
**Funding:** ${c.funding}
### Leadership
${list(c.leadership.map((l) => `${l.name} — ${l.role}`))}
**Hiring Trends:** ${c.hiringTrends}
### Tech Stack
${list(c.techStack)}
**Work Culture:** ${c.culture}
### Interview Experiences
${list(c.interviewExperiences)}
### Competitors
${list(c.competitors)}
---
## 3. Role Intelligence Report — ${r.input.role}
### Required Skills
${list(role.requiredSkills)}
### Frequently Requested Skills
${list(role.frequentSkills)}
### Tools & Technologies
${list([...role.tools, ...role.technologies])}
### Preferred Certifications
${list(role.certifications)}
### Typical Responsibilities
${list(role.responsibilities)}
**Salary Insights:** ${role.salaryInsights}
### Career Growth Paths
${list(role.careerGrowth)}
---
## 4. Skill Gap Analysis & Learning Roadmap
- **Skill Match:** ${s.matchPercent}%
### Matching Skills
${list(s.matchingSkills)}
### Missing Skills
${list(s.missingSkills)}
### 30-Day Plan
${list(s.plan30)}
### 60-Day Plan
${list(s.plan60)}
### 90-Day Plan
${list(s.plan90)}
### Learning Resources
${s.learning
    .map(
      (l) => `**${l.skill}** — ${l.why}
  - Course: ${l.course}
  - YouTube: ${l.youtube}
  - Docs: ${l.documentation}
  - Practice: ${l.practice}
  - Project idea: ${l.projectIdea}`,
    )
    .join("\n\n")}
---
## 5. Interview Preparation Guide
${iv.questions
    .map(
      (q, i) => `### Q${i + 1}. [${q.category} · ${q.difficulty}] ${q.question}
**Model Answer:** ${q.modelAnswer}
**Explanation:** ${q.explanation}
**Tip:** ${q.tip}`,
    )
    .join("\n\n")}
---
## 6. Cover Letters
### ATS-Optimized
${iv.coverLetters.atsOptimized}
### Company-Specific
${iv.coverLetters.companySpecific}
### Short Email Version
${iv.coverLetters.shortEmail}
### Premium Professional Version
${iv.coverLetters.premium}
---
## 7. LinkedIn Optimization Report
**Headline:** ${b.linkedin.headline}
**About:**
${b.linkedin.about}
### Featured Suggestions
${list(b.linkedin.featured)}
### Skills
${list(b.linkedin.skills)}
### Experience Rewrites
${list(b.linkedin.experienceRewrite)}
### SEO Keywords
${list(b.linkedin.seoKeywords)}
---
## 8. Personal Branding Kit
**Tagline:** ${b.branding.tagline}
**Elevator Pitch:** ${b.branding.elevatorPitch}
**Professional Bio:** ${b.branding.professionalBio}
**LinkedIn Post:**
${b.branding.linkedinPost}
**Personal Website Content:**
${b.branding.websiteContent}
**Portfolio Intro:** ${b.branding.portfolioIntro}
**Twitter/X Bio:** ${b.branding.twitterBio}
**GitHub Bio:** ${b.branding.githubBio}
---
## 9. Networking Templates
**Cold Message:** ${b.networking.coldMessage}
**Connection Request:** ${b.networking.connectionRequest}
**Referral Request:** ${b.networking.referralRequest}
**Recruiter Outreach:** ${b.networking.recruiterOutreach}
**Hiring Manager Outreach:** ${b.networking.hiringManagerOutreach}
**Follow-Up:** ${b.networking.followUp}
**Thank You:** ${b.networking.thankYou}
---
## Sources
${list(r.research.sources.map((sc) => `[${sc.title}](${sc.url})`))}
`;
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

export function markdownToHtml(md: string): string {
  const lines = md.split("\n");
  let html = "";
  let inList = false;
  const closeList = () => {
    if (inList) {
      html += "</ul>";
      inList = false;
    }
  };
  for (const raw of lines) {
    const line = raw.replace(/\r$/, "");
    if (/^### /.test(line)) {
      closeList();
      html += `<h3>${inline(line.slice(4))}</h3>`;
    } else if (/^## /.test(line)) {
      closeList();
      html += `<h2>${inline(line.slice(3))}</h2>`;
    } else if (/^# /.test(line)) {
      closeList();
      html += `<h1>${inline(line.slice(2))}</h1>`;
    } else if (/^---\s*$/.test(line)) {
      closeList();
      html += "<hr/>";
    } else if (/^[-*] /.test(line)) {
      if (!inList) {
        html += "<ul>";
        inList = true;
      }
      html += `<li>${inline(line.replace(/^\s*[-*] /, ""))}</li>`;
    } else if (line.trim() === "") {
      closeList();
    } else {
      closeList();
      html += `<p>${inline(line)}</p>`;
    }
  }
  closeList();
  return html;

  function inline(t: string): string {
    return escapeHtml(t)
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/_(.+?)_/g, "<em>$1</em>")
      .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>');
  }
}

function downloadBlob(content: BlobPart, filename: string, type: string) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

export function exportMarkdown(r: CareerReport) {
  downloadBlob(buildMarkdown(r), filename(r, "md"), "text/markdown");
}

const DOC_CSS =
  "body{font-family:Calibri,Arial,sans-serif;color:#1a1a1a;line-height:1.5;}h1{color:#4f46e5;font-size:24pt;}h2{color:#4f46e5;border-bottom:1px solid #ccc;padding-bottom:4px;}h3{color:#0f766e;}a{color:#4f46e5;}hr{border:none;border-top:1px solid #ddd;}li{margin:2px 0;}";

export function exportDocx(r: CareerReport) {
  const body = markdownToHtml(buildMarkdown(r));
  const html = `<!DOCTYPE html><html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word"><head><meta charset="utf-8"><style>${DOC_CSS}</style></head><body>${body}</body></html>`;
  downloadBlob(html, filename(r, "doc"), "application/msword");
}

export function exportPdf(r: CareerReport) {
  const body = markdownToHtml(buildMarkdown(r));
  const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>CareerForge Toolkit</title><style>${DOC_CSS} @page{margin:18mm;}</style></head><body>${body}<script>window.onload=function(){window.print();}</script></body></html>`;
  const w = window.open("", "_blank");
  if (!w) return;
  w.document.write(html);
  w.document.close();
}

function filename(r: CareerReport, ext: string): string {
  const slug = `${r.input.role}-${r.input.company}`
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
  return `careerforge-${slug}.${ext}`;
}
