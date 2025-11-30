import Hero from "../components/Hero";
import SectionWrapper from "../components/SectionWrapper";

export default function Home() {
  return (
    <>
      <Hero />
      <SectionWrapper>
        <h2 className="text-2xl font-semibold mb-2">Welcome to ProDigy GPT-2 Training Platform</h2>
        <p className="text-slate-200 max-w-2xl">
          Train GPT-2 on your domain dataset with an enterprise-ready pipeline including evaluation,
          deployment, monitoring, and safety systems — all through this polished UI.
        </p>
      </SectionWrapper>
    </>
  );
}
