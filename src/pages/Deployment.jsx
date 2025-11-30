import React, { useState } from "react";
import axios from "axios";

export default function Deployment() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const generateText = async () => {
    if (!prompt.trim()) {
      alert("Please enter a prompt!");
      return;
    }

    setLoading(true);
    setResult("");

    try {
      const response = await axios.post("http://localhost:8000/generate", {
        prompt,
      });

      // If backend returns: {"prompt": "...", "responses": ["..."]}
      setResult(response.data.responses?.[0] || "No response");
    } catch (error) {
      console.error(error);
      setResult("❌ Error: Cannot connect to backend");
    }

    setLoading(false);
  };

  return (
    <div className="px-6 py-10 max-w-3xl mx-auto">
      <h1 className="text-4xl font-bold mb-6 text-center">Model Deployment</h1>

      <p className="text-gray-300 mb-4 text-center">
        Enter a prompt below to test your finetuned GPT-2 model.
      </p>

      {/* Textbox */}
      <textarea
        className="w-full h-40 p-4 rounded-lg bg-gray-800 border border-gray-600 text-white focus:outline-none focus:border-blue-400"
        placeholder="Type your prompt here..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      {/* Button */}
      <button
        onClick={generateText}
        className="mt-4 w-full py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-semibold"
      >
        {loading ? "Generating..." : "Generate"}
      </button>

      {/* Output */}
      {result && (
        <div className="mt-6 p-4 bg-gray-800 border border-gray-600 rounded-lg text-white">
          <h2 className="text-xl font-bold mb-2">Generated Output:</h2>
          <p>{result}</p>
        </div>
      )}
    </div>
  );
}
