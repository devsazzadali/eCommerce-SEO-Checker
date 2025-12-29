"use client";
import { useState } from "react";
import AnalyzerForm from "../components/AnalyzerForm";
import ResultsDisplay from "../components/ResultsDisplay";
import AgencyCTA from "../components/AgencyCTA";

export default function Home() {
  const [results, setResults] = useState(null);

  return (
    <main className="min-h-screen bg-slate-50 py-12 px-4 font-sans text-slate-900">
      <div className="max-w-4xl mx-auto text-center mb-12">
        <h1 className="text-5xl font-extrabold mb-4 tracking-tight">
          eCommerce <span className="text-indigo-600">SEO Checker</span>
        </h1>
        <p className="text-xl text-slate-600">
          Instantly audit your product pages. Boost your ranking for free.
        </p>
      </div>

      <AnalyzerForm onResult={setResults} />

      {results && <ResultsDisplay data={results} />}

      <div className="mt-20">
        <AgencyCTA />
      </div>
    </main>
  );
}