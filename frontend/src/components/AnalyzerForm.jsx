"use client";
import { useState } from "react";
import { motion } from "framer-motion";

export default function AnalyzerForm({ onResult }) {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Analysis failed");
      onResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="url"
          required
          placeholder="https://yourstore.com/product-page"
          className="w-full p-4 rounded-xl border-2 border-indigo-100 focus:border-indigo-500 outline-none text-lg text-slate-900 shadow-sm"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          disabled={loading}
          className="bg-indigo-600 text-white font-bold py-4 rounded-xl shadow-lg disabled:opacity-50"
        >
          {loading ? "Analyzing SEO Factors..." : "Check Product SEO"}
        </motion.button>
      </form>
      {error && <p className="text-red-500 mt-4 text-center">{error}</p>}
    </div>
  );
}