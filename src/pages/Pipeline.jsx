import { pipelineSteps } from "../data/pipelineSteps";
import SectionWrapper from "../components/SectionWrapper";

export default function Pipeline() {
  return (
    <SectionWrapper>
      <h1 className="text-3xl font-bold mb-6">Training Pipeline</h1>

      <ul className="space-y-6 text-slate-200">
        {pipelineSteps.map((step, i) => (
          <li key={i}>
            <h3 className="text-xl font-semibold">{step.title}</h3>
            <p className="mt-2">{step.description}</p>
          </li>
        ))}
      </ul>
    </SectionWrapper>
  );
}
