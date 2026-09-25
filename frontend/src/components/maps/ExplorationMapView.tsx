"use client";

import React, { useState } from "react";
import { 
  MapPin, 
  Layers, 
  Info, 
  ShieldAlert, 
  Maximize2, 
  Compass,
  CheckCircle2,
  AlertTriangle
} from "lucide-react";
import { BoreholeRecord } from "@/types/geological";

interface ExplorationMapViewProps {
  boreholes: BoreholeRecord[];
  onSelectBorehole?: (borehole: BoreholeRecord) => void;
}

export const ExplorationMapView: React.FC<ExplorationMapViewProps> = ({
  boreholes,
  onSelectBorehole,
}) => {
  const [activeLayer, setActiveLayer] = useState<"TOPO" | "GEOLOGY" | "CADASTRAL">("GEOLOGY");
  const [selectedPin, setSelectedPin] = useState<string>("BH-NK-094");

  const activeBorehole = boreholes.find((b) => b.boreholeId === selectedPin) || boreholes[0];

  return (
    <div className="space-y-6">
      {/* 1. Header & Layer Control Bar */}
      <div className="bg-white p-4 rounded-lg border border-[#d9e2ec] shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-2">
          <Compass className="w-5 h-5 text-[#121417]" />
          <div>
            <h2 className="font-bold text-base text-[#121417]">
              Cadastral Exploration Map &amp; Stratigraphic Cross-Section
            </h2>
            <p className="text-xs text-slate-500">
              North Karanpura Coalfield • Tandwa Sector (Block IV) • WGS84 / UTM Zone 45N
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2 bg-slate-100 p-1 rounded-md text-xs font-semibold">
          <button
            onClick={() => setActiveLayer("GEOLOGY")}
            className={`px-3 py-1.5 rounded transition-colors ${
              activeLayer === "GEOLOGY" ? "bg-white text-[#0c2340] shadow-sm" : "text-slate-600 hover:text-[#0c2340]"
            }`}
          >
            Geological Strata &amp; Faults
          </button>
          <button
            onClick={() => setActiveLayer("CADASTRAL")}
            className={`px-3 py-1.5 rounded transition-colors ${
              activeLayer === "CADASTRAL" ? "bg-white text-[#0c2340] shadow-sm" : "text-slate-600 hover:text-[#0c2340]"
            }`}
          >
            Cadastral Boundary
          </button>
          <button
            onClick={() => setActiveLayer("TOPO")}
            className={`px-3 py-1.5 rounded transition-colors ${
              activeLayer === "TOPO" ? "bg-white text-[#0c2340] shadow-sm" : "text-slate-600 hover:text-[#0c2340]"
            }`}
          >
            Bhuvan Topo WMS
          </button>
        </div>
      </div>

      {/* 2. Interactive Map & Borehole Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cadastral Map Representation (2 Cols) */}
        <div className="lg:col-span-2 bg-[#0c2340]/5 rounded-lg border border-[#d9e2ec] p-4 relative min-h-[380px] flex flex-col justify-between overflow-hidden shadow-inner bg-slate-900 text-white">
          {/* Spatial Grid Lines Background */}
          <div 
            className="absolute inset-0 opacity-15 pointer-events-none"
            style={{
              backgroundImage: "linear-gradient(to right, #94a3b8 1px, transparent 1px), linear-gradient(to bottom, #94a3b8 1px, transparent 1px)",
              backgroundSize: "40px 40px"
            }}
          />

          {/* Map Top Status */}
          <div className="relative z-10 flex flex-wrap items-center justify-between text-xs bg-slate-900/80 backdrop-blur p-2.5 rounded border border-slate-700 gap-2">
            <div className="flex items-center space-x-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 flex-shrink-0" />
              <span className="font-mono text-[11px] text-slate-300">
                Block IV Grid Coordinates: 23° 48' 10" N, 85° 08' 40" E
              </span>
            </div>
            <div className="flex items-center space-x-2 text-[11px] text-slate-400">
              <span>Datum: WGS84</span>
              <span>•</span>
              <span className="text-amber-400">Fault Buffer: 60m Offset</span>
            </div>
          </div>

          {/* Simulated Borehole Spatial Layout & Cross-Section Line (A - A') */}
          <div className="relative z-10 my-8 h-48 flex items-center justify-around px-8">
            {/* Exploration Cross-Section Line Indicator */}
            <div className="absolute top-1/2 left-8 right-8 h-0.5 border-t-2 border-dashed border-amber-400/80 -translate-y-1/2 pointer-events-none">
              <span className="absolute -top-3.5 left-0 text-[10px] font-bold text-amber-400 bg-slate-900 px-1 rounded">
                Line A
              </span>
              <span className="absolute -top-3.5 right-0 text-[10px] font-bold text-amber-400 bg-slate-900 px-1 rounded">
                Line A'
              </span>
            </div>

            {/* Drillhole Pins */}
            {boreholes.map((b, index) => {
              const isSelected = selectedPin === b.boreholeId;
              const isDiscrepancy = b.statutoryClearance === "FLAGGED_DISCREPANCY";
              return (
                <div
                  key={b.boreholeId}
                  onClick={() => {
                    setSelectedPin(b.boreholeId);
                    if (onSelectBorehole) onSelectBorehole(b);
                  }}
                  className={`relative flex flex-col items-center cursor-pointer transition-transform transform hover:scale-110 ${
                    isSelected ? "scale-110 z-20" : "z-10"
                  }`}
                >
                  <div
                    className={`w-7 h-7 rounded-full flex items-center justify-center font-bold text-[10px] shadow-lg border-2 ${
                      isDiscrepancy
                        ? "bg-amber-500 text-black border-white animate-pulse"
                        : "bg-emerald-600 text-white border-slate-900"
                    }`}
                  >
                    {index + 1}
                  </div>
                  <span className={`text-[10px] font-mono mt-1 px-1.5 py-0.5 rounded ${
                    isSelected ? "bg-amber-400 text-slate-950 font-bold" : "bg-slate-800/80 text-slate-300"
                  }`}>
                    {b.boreholeId}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Map Legend */}
          <div className="relative z-10 flex flex-wrap items-center justify-between text-[11px] bg-slate-900/90 p-2 rounded border border-slate-700 text-slate-300 gap-2">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-1.5">
                <span className="w-3 h-3 rounded-full bg-emerald-600 border border-white" />
                <span>DGMS Cleared Well</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <span className="w-3 h-3 rounded-full bg-amber-500 border border-white" />
                <span>Discrepancy / Joint Review</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <span className="w-4 h-0.5 bg-amber-400 border-t border-dashed" />
                <span>Cross-Section Traverse A - A'</span>
              </div>
            </div>
            <span className="text-slate-500 text-[10px]">CMPDI Survey of India Sheet No: 73E/1</span>
          </div>
        </div>

        {/* Selected Well Summary Card */}
        {activeBorehole && (
          <div className="bg-white rounded-lg border border-[#d9e2ec] p-5 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <span className="text-xs text-slate-500 font-semibold uppercase">Active Well Record</span>
                <h3 className="font-extrabold text-lg text-[#0c2340]">{activeBorehole.boreholeId}</h3>
              </div>
              <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
                activeBorehole.statutoryClearance === "FLAGGED_DISCREPANCY" 
                  ? "bg-amber-100 text-amber-900 border border-amber-300" 
                  : "bg-emerald-100 text-emerald-900 border border-emerald-300"
              }`}>
                {activeBorehole.coalGrade} Coal
              </span>
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Collar Elevation:</span>
                <span className="font-mono font-semibold">{activeBorehole.coordinates.collarElevationMsl} m MSL</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Target Seam Thickness:</span>
                <span className="font-bold text-[#0c2340]">{activeBorehole.targetSeamThickness} m</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Gross Calorific Value:</span>
                <span className="font-mono font-semibold">{activeBorehole.proximateAssay.grossCalorificValueKcal} kcal/kg</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Ash Content:</span>
                <span className="font-mono font-semibold">{activeBorehole.proximateAssay.ashPercent}%</span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-slate-500">Total Drilled Depth:</span>
                <span className="font-mono font-semibold">{activeBorehole.totalDrilledDepthMeters} m</span>
              </div>
            </div>

            {activeBorehole.statutoryClearance === "FLAGGED_DISCREPANCY" ? (
              <div className="p-3 bg-amber-50 border border-amber-200 rounded text-xs text-amber-900 space-y-1">
                <div className="font-bold flex items-center">
                  <AlertTriangle className="w-3.5 h-3.5 text-amber-600 mr-1" />
                  Discrepancy Flagged
                </div>
                <p>MECL (1998) logged 6.80m; revised to 8.42m by CMPDI (2021) sonic log.</p>
              </div>
            ) : (
              <div className="p-3 bg-emerald-50 border border-emerald-200 rounded text-xs text-emerald-900 flex items-center space-x-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                <span>Certified under DGMS CMR 2017 Regulation 113.</span>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 3. 2D Stratigraphic Cross-Section (Line A - A') Rendering (PRD FR-12) */}
      <div className="bg-white rounded-lg border border-[#d9e2ec] p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-200 pb-3">
          <div>
            <h3 className="font-bold text-base text-[#0c2340]">
              Stratigraphic Subsurface Cross-Section (Traverse Line A - A')
            </h3>
            <p className="text-xs text-slate-500">
              Interpolated geological horizons showing Alluvium, Sandstone, Seam IX (8.42m), Interburden, and Seam X
            </p>
          </div>
          <span className="text-xs bg-slate-100 text-slate-700 px-2.5 py-1 rounded font-mono font-semibold">
            Scale: 1:1000 (Vertical Exaggeration: 3x)
          </span>
        </div>

        {/* SVG Stratigraphic Cross-Section Diagram */}
        <div className="w-full bg-slate-50 border border-slate-200 rounded-md p-4 overflow-x-auto">
          <svg viewBox="0 0 800 240" className="w-full min-w-[700px] h-60">
            {/* Ground Level Baseline */}
            <path d="M 50 40 Q 250 35, 450 42 T 750 38" fill="none" stroke="#64748b" strokeWidth="2" />
            <text x="50" y="32" fontSize="10" fill="#475569" fontWeight="bold">Ground Surface (GL: ~482m MSL)</text>

            {/* Layer 1: Alluvium (0 - 42m) */}
            <path d="M 50 40 Q 250 35, 450 42 T 750 38 L 750 78 Q 450 82, 250 76 T 50 78 Z" fill="#fde047" opacity="0.4" />
            <text x="350" y="62" fontSize="11" fill="#854d0e" fontWeight="bold">Alluvium &amp; Weathered Zone (0 – 42.1m)</text>

            {/* Layer 2: Barakar Sandstone (42 - 114m) */}
            <path d="M 50 78 Q 250 76, 450 82 T 750 78 L 750 135 Q 450 140, 250 133 T 50 135 Z" fill="#cbd5e1" opacity="0.6" />
            <text x="320" y="110" fontSize="11" fill="#334155" fontWeight="bold">Barakar Sandstone &amp; Shaly Streaks (42 – 114.3m)</text>

            {/* Layer 3: Target Coal Seam IX (114 - 122m) */}
            <path d="M 50 135 Q 250 133, 450 140 T 750 135 L 750 158 Q 450 162, 250 156 T 50 158 Z" fill="#0f172a" />
            <text x="280" y="150" fontSize="12" fill="#f8fafc" fontWeight="bold">
              ★ Target Coal Seam IX — Verified Thickness: 8.42m (Grade G7)
            </text>

            {/* Layer 4: Interburden (122 - 154m) */}
            <path d="M 50 158 Q 250 156, 450 162 T 750 158 L 750 195 Q 450 198, 250 192 T 50 195 Z" fill="#94a3b8" opacity="0.5" />
            <text x="360" y="180" fontSize="10" fill="#1e293b">Interburden Siliceous Shale (31.4m)</text>

            {/* Layer 5: Coal Seam X (154 - 160m) */}
            <path d="M 50 195 Q 250 192, 450 198 T 750 195 L 750 215 Q 450 218, 250 212 T 50 215 Z" fill="#1e293b" />
            <text x="330" y="208" fontSize="11" fill="#f1f5f9" fontWeight="bold">Coal Seam X Lower Horizon (6.25m, G7)</text>

            {/* Borehole Vertical Traverse Columns */}
            <line x1="200" y1="36" x2="200" y2="225" stroke="#0c2340" strokeWidth="2" strokeDasharray="3,3" />
            <text x="180" y="25" fontSize="10" fill="#0c2340" fontWeight="bold">BH-NK-091</text>

            <line x1="450" y1="42" x2="450" y2="230" stroke="#b06000" strokeWidth="3" />
            <text x="425" y="25" fontSize="10" fill="#b06000" fontWeight="bold">BH-NK-094 (Discrepancy)</text>

            <line x1="650" y1="38" x2="650" y2="225" stroke="#0c2340" strokeWidth="2" strokeDasharray="3,3" />
            <text x="630" y="25" fontSize="10" fill="#0c2340" fontWeight="bold">BH-NK-095</text>

            {/* Fault Line F-1 */}
            <line x1="560" y1="20" x2="520" y2="230" stroke="#ef4444" strokeWidth="2.5" strokeDasharray="4,2" />
            <text x="535" y="80" fontSize="10" fill="#dc2626" fontWeight="bold" transform="rotate(-75, 535, 80)">
              Fault F-1 (Throw: 12m)
            </text>
          </svg>
        </div>
      </div>
    </div>
  );
};
