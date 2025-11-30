export const pipelineSteps = [
  {
    title: "1. Dataset Preparation",
    description:
      "Collect domain text, clean punctuation, convert into JSONL prompt-completion pairs, split train/val/test.",
  },
  {
    title: "2. Training",
    description:
      "Fine-tune GPT-2 using HuggingFace Transformers + Accelerate. Supports FP16, gradient accumulation, and custom training scripts.",
  },
  {
    title: "3. Evaluation",
    description:
      "Compute perplexity, ROUGE, BLEU, and run human-in-the-loop evaluations for generation quality.",
  },
  {
    title: "4. Deployment",
    description:
      "Serve via FastAPI, TorchServe, or Triton. Containerize with Docker and deploy to AWS/GCP/Azure.",
  },
  {
    title: "5. Monitoring",
    description:
      "Track latency, model drift, errors, logs, and user feedback. Integrate Prometheus, Grafana, or W&B.",
  },
];
