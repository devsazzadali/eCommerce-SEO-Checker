"use client";
import { motion } from "framer-motion";

export default function ResultsDisplay({ data }) {
  const getIcon = (status) => {
    if (status === "passed") return "✅";
    if (status === "warning") return "⚠️";
    return "❌";
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-3xl mx-auto mt-12 bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-200"
    >
      <div className="bg-indigo-600 p-8 text-center text-white">
        <h2 className="text-2xl font-bold mb-2">SEO Health Score</h2>
        <div className="text-6xl font-black">{data.score}%</div>
      </div>

      <div className="p-8 space-y-4">
        {data.results.map((item, idx) => (
          <div key={idx} className="flex items-center justify-between p-4 rounded-xl bg-slate-50 border border-slate-100">
            <div className="flex items-center gap-4 text-left">
              <span className="text-2xl">{getIcon(item.status)}</span>
              <div>
                <p className="font-bold text-slate-800">{item.check}</p>
                <p className="text-sm text-slate-500">{item.msg}</p>
              </div>
            </div>
            <span className={`text-[10px] font-bold uppercase px-2 py-1 rounded ${
              item.status === 'passed' ? 'bg-green-100 text-green-700' : 
              item.status === 'warning' ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700'
            }`}>
              {item.status}
            </span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}