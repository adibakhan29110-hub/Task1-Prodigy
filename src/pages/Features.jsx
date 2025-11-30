import FeatureCard from "../components/FeatureCard";
import { FEATURES } from "../data/features";

export default function Features() {
  return (
    <div className="mt-20 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 px-6">
      {FEATURES.map((item, index) => (
        <FeatureCard key={index} {...item} />
      ))}
    </div>
  );
}
