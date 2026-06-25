import {Nav} from "./sections/Nav";
import {Hero} from "./sections/Hero";
import {RecruiterSnapshot} from "./sections/RecruiterSnapshot";
import {GitHubProof} from "./sections/GitHubProof";
import {Projects} from "./sections/Projects";
import {Experience} from "./sections/Experience";
import {Education} from "./sections/Education";
import {TechStack} from "./sections/TechStack";
import {CompanyKnow} from "./sections/CompanyKnow";
import {Contact} from "./sections/Contact";

export default function App() {
  return (
    <div className="min-h-screen overflow-hidden">
      <Nav />
      <main>
        <Hero />
        <RecruiterSnapshot />
        <GitHubProof />
        <Projects />
        <Experience />
        <Education />
        <TechStack />
        <CompanyKnow />
      </main>
      <Contact />
    </div>
  );
}
