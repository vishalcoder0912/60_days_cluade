import { useState, type ReactNode } from "react";
import {
  Bar,
  BarChart,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  Briefcase,
  Building2,
  Download,
  FileText,
  GraduationCap,
  Linkedin,
  MessageSquare,
  RotateCcw,
  Sparkles,
  Target,
} from "lucide-react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { exportDocx, exportMarkdown, exportPdf } from "@/lib/report";
import type { CareerReport } from "@/lib/types";
import { Field, Pills, ScoreRing } from "./shared";

function SectionTitle({ children }: { children: ReactNode }) {
  return <h3 className="mb-3 text-base font-semibold text-foreground">{children}</h3>;
}

export function Dashboard({
  report,
  onReset,
}: {
  report: CareerReport;
  onReset: () => void;
}) {
  const { analysis, research, strategy, interview, branding } = report;
  const [tab, setTab] = useState("resume");
  const keywordData = analysis.keywordMatch.map((k) => ({
    name: k.keyword,
    value: k.present ? 100 : 0,
    present: k.present,
  }));

  return (
    <div className="mx-auto w-full max-w-6xl space-y-6">
      {/* Header */}
      <div className="glass flex flex-col gap-4 rounded-2xl p-5 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Sparkles className="size-4 text-primary" /> Toolkit for {analysis.candidateName}
          </div>
          <h2 className="mt-1 text-xl font-bold">
            {report.input.role} <span className="text-muted-foreground">@</span>{" "}
            <span className="gradient-text">{report.input.company}</span>
          </h2>
          <p className="text-sm text-muted-foreground">
            {report.input.experience} level
            {report.input.location ? ` · ${report.input.location}` : ""}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="secondary" size="sm" onClick={() => exportPdf(report)}>
            <Download className="size-4" /> PDF
          </Button>
          <Button variant="secondary" size="sm" onClick={() => exportDocx(report)}>
            <Download className="size-4" /> DOCX
          </Button>
          <Button variant="secondary" size="sm" onClick={() => exportMarkdown(report)}>
            <Download className="size-4" /> Markdown
          </Button>
          <Button variant="outline" size="sm" onClick={onReset}>
            <RotateCcw className="size-4" /> New
          </Button>
        </div>
      </div>

      {/* Score cards */}
      <div className="grid gap-4 sm:grid-cols-3">
        <Card className="glass">
          <CardContent className="flex items-center justify-center py-6">
            <ScoreRing value={analysis.atsScore} label="ATS Score" />
          </CardContent>
        </Card>
        <Card className="glass">
          <CardContent className="flex items-center justify-center py-6">
            <ScoreRing value={analysis.resumeHealth} label="Resume Health" />
          </CardContent>
        </Card>
        <Card className="glass">
          <CardContent className="flex items-center justify-center py-6">
            <ScoreRing value={strategy.matchPercent} label="Skill Match" />
          </CardContent>
        </Card>
      </div>

      <Tabs value={tab} onValueChange={setTab} className="w-full">
        <TabsList className="flex h-auto w-full flex-wrap justify-start gap-1">
          <TabsTrigger value="resume"><FileText className="size-4" />Resume</TabsTrigger>
          <TabsTrigger value="company"><Building2 className="size-4" />Company</TabsTrigger>
          <TabsTrigger value="role"><Briefcase className="size-4" />Role</TabsTrigger>
          <TabsTrigger value="skills"><Target className="size-4" />Skill Gap</TabsTrigger>
          <TabsTrigger value="interview"><GraduationCap className="size-4" />Interview</TabsTrigger>
          <TabsTrigger value="cover"><FileText className="size-4" />Cover Letters</TabsTrigger>
          <TabsTrigger value="linkedin"><Linkedin className="size-4" />LinkedIn</TabsTrigger>
          <TabsTrigger value="brand"><Sparkles className="size-4" />Branding</TabsTrigger>
          <TabsTrigger value="network"><MessageSquare className="size-4" />Networking</TabsTrigger>
        </TabsList>

        {/* RESUME */}
        <TabsContent value="resume" className="mt-4 space-y-4">
          <Card className="glass">
            <CardHeader><CardTitle>Keyword match</CardTitle></CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={Math.max(180, keywordData.length * 28)}>
                <BarChart data={keywordData} layout="vertical" margin={{ left: 10, right: 16 }}>
                  <XAxis type="number" domain={[0, 100]} hide />
                  <YAxis
                    type="category"
                    dataKey="name"
                    width={140}
                    tick={{ fill: "var(--muted-foreground)", fontSize: 12 }}
                  />
                  <Tooltip
                    cursor={{ fill: "var(--muted)" }}
                    contentStyle={{
                      background: "var(--popover)",
                      border: "1px solid var(--border)",
                      borderRadius: 8,
                      color: "var(--foreground)",
                    }}
                    formatter={(_v, _n, p) => [(p.payload.present ? "Present" : "Missing"), "Status"]}
                  />
                  <Bar dataKey="value" radius={[0, 6, 6, 0]} barSize={16}>
                    {keywordData.map((d, i) => (
                      <Cell key={i} fill={d.present ? "var(--success)" : "var(--destructive)"} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
          <div className="grid gap-4 md:grid-cols-2">
            <Card className="glass">
              <CardHeader><CardTitle className="text-success">Strengths</CardTitle></CardHeader>
              <CardContent><BulletList items={analysis.strengths} /></CardContent>
            </Card>
            <Card className="glass">
              <CardHeader><CardTitle className="text-destructive">Weaknesses</CardTitle></CardHeader>
              <CardContent><BulletList items={analysis.weaknesses} /></CardContent>
            </Card>
          </div>
          <Card className="glass">
            <CardHeader><CardTitle>Improvement suggestions</CardTitle></CardHeader>
            <CardContent><BulletList items={analysis.suggestions} /></CardContent>
          </Card>
          <div className="grid gap-4 md:grid-cols-2">
            <Card className="glass">
              <CardHeader><CardTitle>Extracted skills</CardTitle></CardHeader>
              <CardContent><Pills items={analysis.skills} /></CardContent>
            </Card>
            <Card className="glass">
              <CardHeader><CardTitle>Missing skills & keywords</CardTitle></CardHeader>
              <CardContent className="space-y-3">
                <Pills items={analysis.missingSkills} tone="danger" />
                <Pills items={analysis.missingKeywords} tone="accent" />
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* COMPANY */}
        <TabsContent value="company" className="mt-4 space-y-4">
          <Card className="glass">
            <CardHeader><CardTitle>{report.input.company} overview</CardTitle></CardHeader>
            <CardContent className="space-y-4 text-sm text-muted-foreground">
              <p>{research.company.overview}</p>
              <Field title="Mission">{research.company.mission}</Field>
              <div><SectionTitle>Values</SectionTitle><Pills items={research.company.values} tone="accent" /></div>
              <div><SectionTitle>Tech stack</SectionTitle><Pills items={research.company.techStack} /></div>
              <Field title="Work culture">{research.company.culture}</Field>
              <Field title="Hiring trends">{research.company.hiringTrends}</Field>
              <Field title="Funding">{research.company.funding}</Field>
            </CardContent>
          </Card>
          <div className="grid gap-4 md:grid-cols-2">
            <Card className="glass">
              <CardHeader><CardTitle>Recent news</CardTitle></CardHeader>
              <CardContent><BulletList items={research.company.recentNews} /></CardContent>
            </Card>
            <Card className="glass">
              <CardHeader><CardTitle>Product launches</CardTitle></CardHeader>
              <CardContent><BulletList items={research.company.productLaunches} /></CardContent>
            </Card>
            <Card className="glass">
              <CardHeader><CardTitle>Leadership</CardTitle></CardHeader>
              <CardContent>
                <ul className="space-y-1 text-sm">
                  {research.company.leadership.map((l, i) => (
                    <li key={i}><span className="font-medium text-foreground">{l.name}</span> — {l.role}</li>
                  ))}
                </ul>
              </CardContent>
            </Card>
            <Card className="glass">
              <CardHeader><CardTitle>Interview experiences</CardTitle></CardHeader>
              <CardContent><BulletList items={research.company.interviewExperiences} /></CardContent>
            </Card>
          </div>
          <Card className="glass">
            <CardHeader><CardTitle>Competitors</CardTitle></CardHeader>
            <CardContent><Pills items={research.company.competitors} /></CardContent>
          </Card>
          {research.sources.length > 0 && (
            <Card className="glass">
              <CardHeader><CardTitle>Sources</CardTitle></CardHeader>
              <CardContent>
                <ul className="space-y-1 text-sm">
                  {research.sources.map((s, i) => (
                    <li key={i}>
                      <a href={s.url} target="_blank" rel="noreferrer" className="text-primary hover:underline">{s.title}</a>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* ROLE */}
        <TabsContent value="role" className="mt-4 space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card className="glass"><CardHeader><CardTitle>Required skills</CardTitle></CardHeader><CardContent><Pills items={research.role.requiredSkills} tone="success" /></CardContent></Card>
            <Card className="glass"><CardHeader><CardTitle>Frequently requested</CardTitle></CardHeader><CardContent><Pills items={research.role.frequentSkills} /></CardContent></Card>
            <Card className="glass"><CardHeader><CardTitle>Tools</CardTitle></CardHeader><CardContent><Pills items={research.role.tools} tone="accent" /></CardContent></Card>
            <Card className="glass"><CardHeader><CardTitle>Technologies</CardTitle></CardHeader><CardContent><Pills items={research.role.technologies} tone="accent" /></CardContent></Card>
          </div>
          <Card className="glass"><CardHeader><CardTitle>Typical responsibilities</CardTitle></CardHeader><CardContent><BulletList items={research.role.responsibilities} /></CardContent></Card>
          <div className="grid gap-4 md:grid-cols-2">
            <Card className="glass"><CardHeader><CardTitle>Preferred certifications</CardTitle></CardHeader><CardContent><Pills items={research.role.certifications} /></CardContent></Card>
            <Card className="glass"><CardHeader><CardTitle>Career growth</CardTitle></CardHeader><CardContent><BulletList items={research.role.careerGrowth} /></CardContent></Card>
          </div>
          <Card className="glass"><CardHeader><CardTitle>Salary insights</CardTitle></CardHeader><CardContent className="text-sm text-muted-foreground">{research.role.salaryInsights}</CardContent></Card>
        </TabsContent>

        {/* SKILL GAP */}
        <TabsContent value="skills" className="mt-4 space-y-4">
          <Card className="glass">
            <CardHeader><CardTitle>Skill match: {strategy.matchPercent}%</CardTitle></CardHeader>
            <CardContent className="space-y-4">
              <Progress value={strategy.matchPercent} />
              <div className="grid gap-4 md:grid-cols-2">
                <div><SectionTitle>Matching</SectionTitle><Pills items={strategy.matchingSkills} tone="success" /></div>
                <div><SectionTitle>Missing</SectionTitle><Pills items={strategy.missingSkills} tone="danger" /></div>
              </div>
            </CardContent>
          </Card>
          <div className="grid gap-4 md:grid-cols-3">
            {([["30-Day", strategy.plan30], ["60-Day", strategy.plan60], ["90-Day", strategy.plan90]] as const).map(([title, items]) => (
              <Card key={title} className="glass">
                <CardHeader><CardTitle>{title} plan</CardTitle></CardHeader>
                <CardContent><BulletList items={items} /></CardContent>
              </Card>
            ))}
          </div>
          <Card className="glass">
            <CardHeader><CardTitle>Learning resources</CardTitle></CardHeader>
            <CardContent>
              <Accordion type="single" collapsible className="w-full">
                {strategy.learning.map((l, i) => (
                  <AccordionItem key={i} value={`l-${i}`}>
                    <AccordionTrigger>{l.skill}</AccordionTrigger>
                    <AccordionContent className="space-y-2 text-sm">
                      <p className="text-muted-foreground">{l.why}</p>
                      <ul className="space-y-1">
                        <li><strong>Course:</strong> {l.course}</li>
                        <li><strong>YouTube:</strong> {l.youtube}</li>
                        <li><strong>Docs:</strong> {l.documentation}</li>
                        <li><strong>Practice:</strong> {l.practice}</li>
                        <li><strong>Project idea:</strong> {l.projectIdea}</li>
                      </ul>
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            </CardContent>
          </Card>
        </TabsContent>

        {/* INTERVIEW */}
        <TabsContent value="interview" className="mt-4 space-y-3">
          <Accordion type="single" collapsible className="w-full space-y-2">
            {interview.questions.map((q, i) => (
              <AccordionItem key={i} value={`q-${i}`} className="glass rounded-xl border px-4">
                <AccordionTrigger className="text-left">
                  <span className="flex flex-wrap items-center gap-2">
                    <Badge variant="secondary">{q.category}</Badge>
                    <Badge variant="outline">{q.difficulty}</Badge>
                    <span>{q.question}</span>
                  </span>
                </AccordionTrigger>
                <AccordionContent className="space-y-2 text-sm">
                  <p><strong className="text-foreground">Model answer:</strong> <span className="text-muted-foreground">{q.modelAnswer}</span></p>
                  <p><strong className="text-foreground">Explanation:</strong> <span className="text-muted-foreground">{q.explanation}</span></p>
                  <p><strong className="text-accent">Tip:</strong> <span className="text-muted-foreground">{q.tip}</span></p>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </TabsContent>

        {/* COVER LETTERS */}
        <TabsContent value="cover" className="mt-4 grid gap-4 md:grid-cols-2">
          <Field title="ATS-optimized" copy={interview.coverLetters.atsOptimized}><pre className="whitespace-pre-wrap font-sans">{interview.coverLetters.atsOptimized}</pre></Field>
          <Field title="Company-specific" copy={interview.coverLetters.companySpecific}><pre className="whitespace-pre-wrap font-sans">{interview.coverLetters.companySpecific}</pre></Field>
          <Field title="Short email" copy={interview.coverLetters.shortEmail}><pre className="whitespace-pre-wrap font-sans">{interview.coverLetters.shortEmail}</pre></Field>
          <Field title="Premium professional" copy={interview.coverLetters.premium}><pre className="whitespace-pre-wrap font-sans">{interview.coverLetters.premium}</pre></Field>
        </TabsContent>

        {/* LINKEDIN */}
        <TabsContent value="linkedin" className="mt-4 space-y-4">
          <Field title="Optimized headline" copy={branding.linkedin.headline}>{branding.linkedin.headline}</Field>
          <Field title="About section" copy={branding.linkedin.about}><pre className="whitespace-pre-wrap font-sans">{branding.linkedin.about}</pre></Field>
          <div className="grid gap-4 md:grid-cols-2">
            <Card className="glass"><CardHeader><CardTitle>Featured suggestions</CardTitle></CardHeader><CardContent><BulletList items={branding.linkedin.featured} /></CardContent></Card>
            <Card className="glass"><CardHeader><CardTitle>Skills</CardTitle></CardHeader><CardContent><Pills items={branding.linkedin.skills} /></CardContent></Card>
          </div>
          <Card className="glass"><CardHeader><CardTitle>Experience rewrites</CardTitle></CardHeader><CardContent><BulletList items={branding.linkedin.experienceRewrite} /></CardContent></Card>
          <Card className="glass"><CardHeader><CardTitle>SEO keywords</CardTitle></CardHeader><CardContent><Pills items={branding.linkedin.seoKeywords} tone="accent" /></CardContent></Card>
        </TabsContent>

        {/* BRANDING */}
        <TabsContent value="brand" className="mt-4 grid gap-4 md:grid-cols-2">
          <Field title="Professional tagline" copy={branding.branding.tagline}>{branding.branding.tagline}</Field>
          <Field title="Elevator pitch" copy={branding.branding.elevatorPitch}>{branding.branding.elevatorPitch}</Field>
          <Field title="Professional bio" copy={branding.branding.professionalBio}>{branding.branding.professionalBio}</Field>
          <Field title="Portfolio intro" copy={branding.branding.portfolioIntro}>{branding.branding.portfolioIntro}</Field>
          <Field title="LinkedIn post" copy={branding.branding.linkedinPost}><pre className="whitespace-pre-wrap font-sans">{branding.branding.linkedinPost}</pre></Field>
          <Field title="Personal website content" copy={branding.branding.websiteContent}><pre className="whitespace-pre-wrap font-sans">{branding.branding.websiteContent}</pre></Field>
          <Field title="Twitter / X bio" copy={branding.branding.twitterBio}>{branding.branding.twitterBio}</Field>
          <Field title="GitHub bio" copy={branding.branding.githubBio}>{branding.branding.githubBio}</Field>
        </TabsContent>

        {/* NETWORKING */}
        <TabsContent value="network" className="mt-4 grid gap-4 md:grid-cols-2">
          <Field title="Cold message" copy={branding.networking.coldMessage}><pre className="whitespace-pre-wrap font-sans">{branding.networking.coldMessage}</pre></Field>
          <Field title="Connection request" copy={branding.networking.connectionRequest}><pre className="whitespace-pre-wrap font-sans">{branding.networking.connectionRequest}</pre></Field>
          <Field title="Referral request" copy={branding.networking.referralRequest}><pre className="whitespace-pre-wrap font-sans">{branding.networking.referralRequest}</pre></Field>
          <Field title="Recruiter outreach" copy={branding.networking.recruiterOutreach}><pre className="whitespace-pre-wrap font-sans">{branding.networking.recruiterOutreach}</pre></Field>
          <Field title="Hiring manager outreach" copy={branding.networking.hiringManagerOutreach}><pre className="whitespace-pre-wrap font-sans">{branding.networking.hiringManagerOutreach}</pre></Field>
          <Field title="Follow-up" copy={branding.networking.followUp}><pre className="whitespace-pre-wrap font-sans">{branding.networking.followUp}</pre></Field>
          <Field title="Thank you" copy={branding.networking.thankYou}><pre className="whitespace-pre-wrap font-sans">{branding.networking.thankYou}</pre></Field>
        </TabsContent>
      </Tabs>
    </div>
  );
}

function BulletList({ items }: { items: string[] }) {
  if (!items?.length) return <p className="text-sm text-muted-foreground">None listed.</p>;
  return (
    <ul className="space-y-1.5 text-sm text-muted-foreground">
      {items.map((it, i) => (
        <li key={i} className="flex gap-2">
          <span className="mt-1.5 size-1.5 shrink-0 rounded-full bg-primary" />
          <span>{it}</span>
        </li>
      ))}
    </ul>
  );
}
