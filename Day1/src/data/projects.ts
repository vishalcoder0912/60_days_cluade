export type Project = {
  name: string;
  label: string;
  description: string;
  tags: string[];
  github: string;
  highlight?: string;
  links?: {label: string; href: string}[];
};

export const projects: Project[] = [
  {
    name: "freelance",
    label: "Daily Build Repository",
    github: "https://github.com/vishalcoder0912/freelance",
    description:
      "Current daily working repository focused on school management modules, child-friendly dashboards, interactive learning games, progress tracking, and UI improvements.",
    tags: ["React", "TypeScript", "Tailwind CSS", "Education Platform", "UI/UX", "Daily Builds"],
    highlight: "Latest active work repository",
  },
  {
    name: "Gilded Bites",
    label: "Luxury Chocolate E-Commerce / Full-Stack Product",
    github: "https://github.com/vishalcoder0912/gilded-bites",
    description:
      "Luxury chocolate e-commerce/full-stack product concept with modern frontend, backend scripts, Prisma, Firebase, Stripe, Three.js, Framer Motion, GSAP, Zustand, and React Query.",
    tags: ["React", "TypeScript", "Vite", "Express", "Prisma", "PostgreSQL", "Firebase", "Stripe", "Three.js", "GSAP"],
  },
  {
    name: "Freelance Project 4",
    label: "Freelance Website Build",
    github: "https://github.com/vishalcoder0912/freelance/blob/main/project%204/index.html",
    description:
      "A focused website build from the active freelance repository, showing practical frontend implementation, page structure, responsive layout work, and daily production-style improvements.",
    tags: ["HTML", "CSS", "JavaScript", "Frontend", "Freelance Work", "Responsive Website", "UI/UX"],
  },
  {
    name: "Agentic AI Data Analysis",
    label: "AI Analytics Platform",
    github: "https://github.com/vishalcoder0912/Analytics-api",
    description:
      "Schema-first analytics platform concept with dataset upload, KPI generation, dashboards, chart creation, and natural-language data questions.",
    tags: ["AI", "Analytics", "Python", "Dashboards", "Data Visualization", "APIs"],
    links: [
      {label: "insightflow-ai", href: "https://github.com/vishalcoder0912/insightflow-ai"},
      {label: "insightflow-ai-1", href: "https://github.com/vishalcoder0912/insightflow-ai-1"},
    ],
  },
  {
    name: "Little Stars Academy Playground",
    label: "School / Kids Learning Platform",
    github: "https://github.com/vishalcoder0912/little-stars-academy-playground",
    description:
      "Child-friendly education platform concept for early learning with dashboards, interactive activities, class modules, and parent/teacher focused features.",
    tags: ["React", "TypeScript", "Education", "Kids Learning", "Dashboard UI"],
  },
  {
    name: "Choco Sphere",
    label: "Premium Chocolate Web Experience",
    github: "https://github.com/vishalcoder0912/choco-sphere",
    description:
      "Premium chocolate web experience focused on landing page design, product storytelling, visual polish, and conversion-focused frontend layout.",
    tags: ["React", "TypeScript", "Landing Page", "E-Commerce UI", "Product Design"],
  },
];
