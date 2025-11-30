import { motion } from "framer-motion";

export default function Hero() {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7 }}
      className="px-6 pt-20"
    >
      <h1 className="text-4xl sm:text-5xl font-bold max-w-3xl leading-tight">
        Train GPT-2 to generate coherent, context-aware text for your domain
      </h1>

      <p className="mt-4 text-slate-200 max-w-xl">
        Fine-tune GPT-2 using a full industry-grade pipeline. Clean data, train,
        evaluate, deploy, monitor — all structured, scalable, and production-ready.
      </p>
    </motion.div>
  );
}
