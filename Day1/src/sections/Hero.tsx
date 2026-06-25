import {ArrowDownRight, MapPin} from "lucide-react";
import {motion} from "framer-motion";
import {Button} from "../components/Button";
import {StatBadge} from "../components/StatBadge";
import {profile} from "../data/profile";
import {heroStats} from "../data/stats";

export function Hero() {
  return (
    <section id="top" className="container-sketch relative pb-16 pt-12 sm:pt-16">
      <div className="grid items-center gap-10 lg:grid-cols-[0.82fr_1.18fr]">
        <motion.figure
          initial={{opacity: 0, y: 18, rotate: -3}}
          animate={{opacity: 1, y: 0, rotate: -2}}
          transition={{duration: 0.45}}
          className="relative mx-auto w-full max-w-md rounded-[42px_18px_34px_22px/20px_42px_18px_36px] border-[3px] border-ink bg-white p-4 shadow-hardLg"
        >
          <span className="absolute left-1/2 top-0 z-10 h-9 w-32 -translate-x-1/2 -translate-y-5 rotate-2 border-x-2 border-dashed border-ink/30 bg-muted/90" aria-hidden="true" />
          <div className="relative aspect-[3/4] overflow-hidden rounded-[28px_14px_24px_18px/16px_32px_18px_28px] border-[3px] border-ink bg-muted">
            <img className="h-full w-full object-cover object-[center_18%]" src={profile.image} alt={`Portrait of ${profile.name}`} />
            <span className="absolute inset-3 rounded-[28px_14px_24px_18px/16px_32px_18px_28px] border-2 border-dashed border-ink/25" aria-hidden="true" />
          </div>
          <figcaption className="flex items-center justify-between gap-3 px-1 pt-4 text-xl leading-none">
            <span>{profile.role}</span>
            <span className="h-5 w-5 rounded-full border-2 border-ink bg-marker shadow-[2px_2px_0_0_#2d2d2d]" aria-hidden="true" />
          </figcaption>
        </motion.figure>

        <motion.div initial={{opacity: 0, y: 18}} animate={{opacity: 1, y: 0}} transition={{duration: 0.45, delay: 0.08}}>
          <div className="mb-4 inline-flex -rotate-1 items-center gap-2 rounded-wobbly border-[3px] border-ink bg-white px-4 py-2 font-heading text-2xl leading-none text-pen shadow-hard">
            <MapPin size={22} strokeWidth={2.8} />
            {profile.location} / Open To Work
          </div>
          <h1 className="max-w-4xl font-heading text-4xl leading-[0.98] sm:text-5xl lg:text-6xl">
            Full-Stack MERN Developer building AI apps, dashboards, landing pages, and product-ready web experiences<span className="inline-block rotate-12 text-marker">!</span>
          </h1>
          <p className="mt-6 max-w-3xl border-l-4 border-dashed border-marker pl-5 text-2xl leading-snug sm:text-3xl">
            I build responsive web apps, AI-powered tools, landing pages, dashboards, and MERN products that companies can understand, test, and ship.
          </p>
          <div className="mt-7 flex flex-wrap gap-4">
            <Button href="#contact">Contact Me</Button>
            <Button href="#projects" variant="secondary">
              View Projects
            </Button>
          </div>
        </motion.div>
      </div>

      <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {heroStats.map((stat) => (
          <StatBadge key={stat.label} {...stat} />
        ))}
      </div>
      <ArrowDownRight className="absolute right-8 top-[38rem] hidden animate-bob text-ink/70 lg:block" size={90} strokeWidth={1.7} />
    </section>
  );
}
