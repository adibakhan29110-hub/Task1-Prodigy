import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import GradientCircles from "./components/GradientCircles";
import Footer from "./components/Footer";

import Home from "./pages/Home";
import Features from "./pages/Features";
import Pipeline from "./pages/Pipeline";
import Deployment from "./pages/Deployment";

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-900 via-sky-800 to-indigo-900 text-white relative">
      <Router>

        <GradientCircles />
        <Navbar />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/features" element={<Features />} />
          <Route path="/pipeline" element={<Pipeline />} />
          <Route path="/deployment" element={<Deployment />} />
        </Routes>

        <Footer />
      </Router>
    </div>
  );
}
