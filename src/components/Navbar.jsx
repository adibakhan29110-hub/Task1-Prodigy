import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between px-6 py-4 bg-white/10 backdrop-blur-lg border-b border-white/10">
      <h1 className="text-lg font-bold">ProDigy Infotech</h1>

      <div className="space-x-6">
        <Link to="/">Home</Link>
        <Link to="/features">Features</Link>
        <Link to="/pipeline">Pipeline</Link>
        <Link to="/deployment">Deployment</Link>
      </div>
    </nav>
  );
}
