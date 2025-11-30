export default function FeatureCard({ tag, title, desc }) {
  return (
    <div className="p-6 bg-white/10 rounded-2xl border border-white/10 hover:scale-[1.02] transition">
      <div className="text-xs uppercase text-sky-200">{tag}</div>
      <h4 className="mt-2 text-lg font-semibold">{title}</h4>
      <p className="mt-3 text-sm text-slate-200">{desc}</p>
    </div>
  );
}
