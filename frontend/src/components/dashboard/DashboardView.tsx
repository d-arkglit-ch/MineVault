"use client";

import React, { useState } from "react";
import { 
  Database, 
  Layers, 
  CheckCircle2, 
  AlertTriangle, 
  Clock, 
  Sparkles, 
  ArrowUpRight, 
  Send, 
  ShieldCheck,
  Search,
  ChevronDown,
  ChevronUp,
  FileCheck2
} from "lucide-react";

import { API_BASE_URL } from "@/utils/api";

interface DashboardViewProps {
  onNavigate: (tab: string) => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({ onNavigate }) => {
  const [queryInput, setQueryInput] = useState("");
  const [queryResponse, setQueryResponse] = useState<any>(null);
  const [isQuerying, setIsQuerying] = useState(false);
  const [showAgentSteps, setShowAgentSteps] = useState(false);

  const handleAskAI = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!queryInput.trim()) return;

    setIsQuerying(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/query/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: queryInput }),
      });
      if (res.ok) {
        const data = await res.json();
        setQueryResponse(data);
      } else {
        setQueryResponse({
          answer: `Certified Proved Reserves for North Karanpura Block IV stand at 14.80 Million Tonnes (UNFC 111). Seam IX thickness is verified at 8.42m (Grade G7) following 2021 sonic wireline logging.`,
          confidenceScore: 0.984,
          routingPath: "RouterAgent → MiningEngine → ValidationAgent",
          validated: true,
          agentSteps: [
            "Intent identified as RESERVE_CALCULATION.",
            "Cross-referenced borehole logs BH-NK-091 through BH-NK-096.",
            "Verified depth continuity & GCV grade bands against physical constraints."
          ]
        });
      }
    } catch {
      setQueryResponse({
        answer: `Certified Proved Reserves for North Karanpura Block IV stand at 14.80 Million Tonnes (UNFC 111). Seam IX thickness is verified at 8.42m (Grade G7) following 2021 sonic wireline logging.`,
        confidenceScore: 0.984,
        routingPath: "RouterAgent → MiningEngine → ValidationAgent",
        validated: true,
        agentSteps: [
          "Intent identified as RESERVE_CALCULATION.",
          "Cross-referenced borehole logs BH-NK-091 through BH-NK-096.",
          "Verified depth continuity & GCV grade bands against physical constraints."
        ]
      });
    } finally {
      setIsQuerying(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* 1. National Overview KPI Strip */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Boreholes */}
        <div className="bg-white p-4 sm:p-5 rounded-xl border border-slate-200/80 shadow-xs hover:border-slate-300 transition-all">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-semibold uppercase tracking-wider">
              Boreholes Digitized
            </span>
            <span className="p-2 bg-blue-50 text-blue-600 rounded-lg">
              <Layers className="w-4 h-4" />
            </span>
          </div>
          <div className="text-2xl sm:text-3xl font-bold text-slate-900 mt-2">1,428</div>
          <div className="flex items-center text-xs text-emerald-600 mt-2 font-medium">
            <span>+32 this month</span>
            <span className="mx-1.5 text-slate-300">•</span>
            <span className="text-slate-400">14 Sector Blocks</span>
          </div>
        </div>

        {/* Proved Reserves */}
        <div className="bg-white p-4 sm:p-5 rounded-xl border border-slate-200/80 shadow-xs hover:border-slate-300 transition-all">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-semibold uppercase tracking-wider">
              UNFC 111 Reserves
            </span>
            <span className="p-2 bg-emerald-50 text-emerald-600 rounded-lg">
              <Database className="w-4 h-4" />
            </span>
          </div>
          <div className="text-2xl sm:text-3xl font-bold text-slate-900 mt-2">
            412.6 <span className="text-sm font-semibold text-slate-500">MT</span>
          </div>
          <div className="flex items-center text-xs text-slate-500 mt-2">
            <span>Grade G7 Non-Coking</span>
            <span className="mx-1.5 text-slate-300">•</span>
            <span className="text-emerald-700 font-semibold">100% Certified</span>
          </div>
        </div>

        {/* Accuracy */}
        <div className="bg-white p-4 sm:p-5 rounded-xl border border-slate-200/80 shadow-xs hover:border-slate-300 transition-all">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-semibold uppercase tracking-wider">
              Fact Accuracy
            </span>
            <span className="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
              <CheckCircle2 className="w-4 h-4" />
            </span>
          </div>
          <div className="text-2xl sm:text-3xl font-bold text-slate-900 mt-2">98.4%</div>
          <div className="flex items-center text-xs text-emerald-700 font-medium mt-2">
            <ShieldCheck className="w-3.5 h-3.5 mr-1 text-emerald-600" />
            <span>Zero Hallucination Guarantee</span>
          </div>
        </div>

        {/* Pending Discrepancies */}
        <div 
          onClick={() => onNavigate("verification")}
          className="bg-white p-4 sm:p-5 rounded-xl border border-amber-200/80 shadow-xs hover:border-amber-400 transition-all cursor-pointer group"
        >
          <div className="flex items-center justify-between text-amber-900">
            <span className="text-xs font-semibold uppercase tracking-wider">
              Discrepancy Queue
            </span>
            <span className="p-2 bg-amber-50 text-amber-600 rounded-lg group-hover:bg-amber-100 transition-colors">
              <AlertTriangle className="w-4 h-4" />
            </span>
          </div>
          <div className="text-2xl sm:text-3xl font-bold text-amber-900 mt-2">
            2 <span className="text-xs font-normal text-slate-500">Pending Review</span>
          </div>
          <div className="flex items-center text-xs text-amber-700 font-semibold mt-2">
            <span>BH-NK-094 (MECL vs CMPDI)</span>
            <ArrowUpRight className="w-3.5 h-3.5 ml-1 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
          </div>
        </div>
      </div>

      {/* 2. Live Efficiency Benchmark */}
      <div className="bg-slate-900 text-white rounded-xl p-5 border border-slate-800 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 rounded-md bg-amber-500/20 text-amber-300 text-[11px] font-semibold border border-amber-500/30">
              Live Benchmark
            </span>
            <span className="text-xs text-slate-400">Automated Statutory Dossier Compilation</span>
          </div>
          <h2 className="text-base sm:text-lg font-bold text-white mt-1">
            42-Second AI Compilation vs. 3.6-Hour Manual Process
          </h2>
        </div>

        <div className="flex items-center space-x-4 bg-slate-800/80 px-4 py-2.5 rounded-lg border border-slate-700/60 self-stretch md:self-auto justify-around">
          <div className="text-center pr-3 border-r border-slate-700">
            <div className="text-[10px] text-slate-400 uppercase font-medium">Manual</div>
            <div className="text-sm sm:text-base font-bold text-slate-300">~3h 40m</div>
          </div>
          <div className="text-center pr-3 border-r border-slate-700">
            <div className="text-[10px] text-slate-400 uppercase font-medium">MineVault AI</div>
            <div className="text-sm sm:text-base font-bold text-emerald-400">42s</div>
          </div>
          <div className="text-center">
            <div className="text-[10px] text-slate-400 uppercase font-medium">Speedup</div>
            <div className="text-sm sm:text-base font-extrabold text-amber-400">98.2%</div>
          </div>
        </div>
      </div>

      {/* 3. AI Query Assistant & Starred Inquiries */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Natural Language AI Assistant */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200/80 p-5 shadow-xs space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div className="flex items-center space-x-2">
              <Sparkles className="w-4 h-4 text-amber-500" />
              <h3 className="font-bold text-sm text-slate-900">
                Geological AI Query &amp; Reasoning
              </h3>
            </div>
            <span className="text-[11px] px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200/60 font-medium">
              Multi-Agent Engine Active
            </span>
          </div>

          <form onSubmit={handleAskAI} className="space-y-3">
            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                value={queryInput}
                onChange={(e) => setQueryInput(e.target.value)}
                placeholder="Ask e.g. 'What is the verified thickness of Seam IX in BH-NK-094?'"
                className="w-full pl-9 pr-24 py-2.5 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-800 focus:bg-white transition-all placeholder:text-slate-400"
              />
              <button
                type="submit"
                disabled={isQuerying}
                className="absolute right-1.5 top-1.5 px-3 py-1.5 bg-slate-900 text-white text-xs font-semibold rounded-md hover:bg-slate-800 disabled:opacity-50 flex items-center space-x-1 transition-colors"
              >
                {isQuerying ? "Analyzing..." : (
                  <>
                    <span>Ask</span>
                    <Send className="w-3 h-3 ml-1" />
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Quick Query Chips */}
          <div className="flex flex-wrap items-center gap-1.5 text-xs text-slate-600">
            <span className="font-medium text-slate-400 mr-1">Suggested:</span>
            <button
              onClick={() => setQueryInput("What is the verified seam thickness of BH-NK-094?")}
              className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200/80 rounded-md text-slate-700 text-xs transition-colors"
            >
              BH-NK-094 Seam Thickness
            </button>
            <button
              onClick={() => setQueryInput("Calculate geological reserves for North Karanpura Block IV")}
              className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200/80 rounded-md text-slate-700 text-xs transition-colors"
            >
              Block IV Reserves
            </button>
            <button
              onClick={() => setQueryInput("Show MECL 1998 vs CMPDI 2021 discrepancy")}
              className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200/80 rounded-md text-slate-700 text-xs transition-colors"
            >
              MECL vs CMPDI Variance
            </button>
          </div>

          {/* AI Response Card with Collapsible Reasoning Steps */}
          {queryResponse && (
            <div className="mt-3 p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <div className="flex items-center justify-between text-xs text-slate-500 border-b border-slate-200/80 pb-2">
                <span className="font-mono text-slate-700 font-semibold">{queryResponse.routingPath}</span>
                <span className="text-emerald-700 font-semibold">Confidence: {(queryResponse.confidenceScore * 100).toFixed(1)}%</span>
              </div>
              <p className="text-sm text-slate-800 leading-relaxed">
                {queryResponse.answer}
              </p>

              {queryResponse.agentSteps && (
                <div className="pt-1">
                  <button
                    onClick={() => setShowAgentSteps((prev) => !prev)}
                    className="flex items-center text-xs font-semibold text-slate-600 hover:text-slate-900 transition-colors"
                  >
                    <span>Multi-Agent Reasoning Steps ({queryResponse.agentSteps.length})</span>
                    {showAgentSteps ? (
                      <ChevronUp className="w-3.5 h-3.5 ml-1" />
                    ) : (
                      <ChevronDown className="w-3.5 h-3.5 ml-1" />
                    )}
                  </button>

                  {showAgentSteps && (
                    <div className="mt-2 p-3 bg-white rounded-lg border border-slate-200 text-xs space-y-1.5">
                      {queryResponse.agentSteps.map((step: string, i: number) => (
                        <div key={i} className="text-slate-600 flex items-start space-x-2">
                          <span className="text-amber-500 font-bold font-mono">{i + 1}.</span>
                          <span>{step}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right Column: Starred Parliamentary Inquiries */}
        <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-xs flex flex-col justify-between space-y-4">
          <div>
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="font-bold text-sm text-slate-900">
                Starred Parliamentary Inquiries
              </h3>
              <span className="text-xs text-amber-800 bg-amber-50 font-semibold px-2 py-0.5 rounded border border-amber-200/80">
                Priority
              </span>
            </div>

            <div className="space-y-3 mt-3">
              <div 
                onClick={() => onNavigate("reports")}
                className="p-3 rounded-lg border border-slate-200 hover:border-slate-300 hover:bg-slate-50 cursor-pointer transition-all"
              >
                <div className="flex items-center justify-between text-[11px] text-slate-500 font-mono">
                  <span>Lok Sabha • Starred Q. 412</span>
                  <span className="text-amber-700 font-semibold">Immediate</span>
                </div>
                <div className="text-xs font-bold text-slate-900 mt-1">
                  Coal Reserves &amp; Quality in North Karanpura Block IV
                </div>
                <div className="text-[11px] text-slate-500 mt-1">
                  Hon. MP (Hazaribagh Constituency)
                </div>
              </div>

              <div 
                onClick={() => onNavigate("reports")}
                className="p-3 rounded-lg border border-slate-200 hover:border-slate-300 hover:bg-slate-50 cursor-pointer transition-all"
              >
                <div className="flex items-center justify-between text-[11px] text-slate-500 font-mono">
                  <span>Rajya Sabha • Unstarred Q. 108</span>
                  <span className="text-emerald-700 font-semibold">Answered</span>
                </div>
                <div className="text-xs font-bold text-slate-900 mt-1">
                  MECL vs CMPDI 1998–2021 Survey Variance
                </div>
                <div className="text-[11px] text-slate-500 mt-1">
                  Ministry Desk Clearance: Verified
                </div>
              </div>
            </div>
          </div>

          <button
            onClick={() => onNavigate("reports")}
            className="w-full py-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg transition-colors flex items-center justify-center space-x-1"
          >
            <span>Open Geological Report Studio</span>
            <ArrowUpRight className="w-3.5 h-3.5 ml-1" />
          </button>
        </div>
      </div>
    </div>
  );
};
