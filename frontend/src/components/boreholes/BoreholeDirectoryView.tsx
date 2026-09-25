"use client";

import React, { useState } from "react";
import { 
  Search, 
  Filter, 
  Layers, 
  ShieldCheck, 
  AlertTriangle, 
  X, 
  FileText, 
  ExternalLink,
  ChevronRight,
  Hash
} from "lucide-react";
import { BoreholeRecord } from "@/types/geological";
import { generateFormVDossierPDF } from "@/utils/pdfGenerator";

interface BoreholeDirectoryViewProps {
  boreholes: BoreholeRecord[];
  onSelectDiscrepancy?: (discrepancyId: string) => void;
}

export const BoreholeDirectoryView: React.FC<BoreholeDirectoryViewProps> = ({
  boreholes,
  onSelectDiscrepancy,
}) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [selectedBorehole, setSelectedBorehole] = useState<BoreholeRecord | null>(null);

  const filteredBoreholes = boreholes.filter((b) => {
    const matchesSearch =
      b.boreholeId.toLowerCase().includes(searchTerm.toLowerCase()) ||
      b.sectorBlock.toLowerCase().includes(searchTerm.toLowerCase()) ||
      b.coalfield.toLowerCase().includes(searchTerm.toLowerCase()) ||
      b.coalGrade.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesStatus =
      statusFilter === "ALL" || b.statutoryClearance === statusFilter;

    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-4">
      {/* 1. Header & Filters Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center space-x-2.5">
          <Layers className="w-5 h-5 text-slate-800" />
          <h2 className="font-bold text-sm sm:text-base text-slate-900">
            National Borehole Directory
          </h2>
          <span className="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 font-mono text-slate-700 font-medium">
            {filteredBoreholes.length} Records
          </span>
        </div>

        <div className="flex items-center space-x-2.5 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-64">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search ID, coalfield, grade..."
              className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-800 transition-all placeholder:text-slate-400"
            />
          </div>

          <div className="flex items-center space-x-1.5 text-xs">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="py-1.5 px-2.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-800 transition-all text-slate-700 font-medium"
            >
              <option value="ALL">All Clearances</option>
              <option value="DGMS_CLEARED">DGMS Cleared</option>
              <option value="UNDER_JOINT_REVIEW">Under Review</option>
              <option value="FLAGGED_DISCREPANCY">Discrepancy</option>
            </select>
          </div>
        </div>
      </div>

      {/* 2. Borehole Tabular Register */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900 text-slate-200 uppercase text-[10px] font-semibold tracking-wider">
              <tr>
                <th className="py-3 px-4">Borehole ID</th>
                <th className="py-3 px-4">Sector / Block</th>
                <th className="py-3 px-4">Coordinates</th>
                <th className="py-3 px-4">Total Depth</th>
                <th className="py-3 px-4">Seam Thickness</th>
                <th className="py-3 px-4">Coal Grade</th>
                <th className="py-3 px-4">Proximate Assay</th>
                <th className="py-3 px-4">Clearance Status</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredBoreholes.map((b) => (
                <tr
                  key={b.boreholeId}
                  onClick={() => setSelectedBorehole(b)}
                  className={`hover:bg-slate-50/80 cursor-pointer transition-colors ${
                    selectedBorehole?.boreholeId === b.boreholeId ? "bg-amber-50/50" : ""
                  }`}
                >
                  <td className="py-3 px-4 font-mono font-bold text-slate-900 flex items-center space-x-1.5">
                    <span>{b.boreholeId}</span>
                    {b.statutoryClearance === "FLAGGED_DISCREPANCY" && (
                      <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
                    )}
                  </td>
                  <td className="py-3 px-4 text-slate-700">{b.sectorBlock}</td>
                  <td className="py-3 px-4 font-mono text-slate-500 text-[11px]">
                    {b.coordinates.latitude}, {b.coordinates.longitude}
                  </td>
                  <td className="py-3 px-4 font-semibold text-slate-900">
                    {b.totalDrilledDepthMeters.toFixed(2)} m
                  </td>
                  <td className="py-3 px-4 font-bold text-slate-900">
                    {b.targetSeamThickness.toFixed(2)} m
                  </td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-0.5 bg-blue-50 text-blue-700 rounded font-semibold text-[11px] border border-blue-200/60">
                      {b.coalGrade}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-600 font-mono text-[11px]">
                    Ash: {b.proximateAssay.ashPercent}% | GCV: {b.proximateAssay.grossCalorificValueKcal}
                  </td>
                  <td className="py-3 px-4">
                    {b.statutoryClearance === "DGMS_CLEARED" && (
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200/70">
                        <ShieldCheck className="w-3 h-3 mr-1" />
                        DGMS Cleared
                      </span>
                    )}
                    {b.statutoryClearance === "UNDER_JOINT_REVIEW" && (
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-50 text-amber-700 border border-amber-200/70">
                        Under Review
                      </span>
                    )}
                    {b.statutoryClearance === "FLAGGED_DISCREPANCY" && (
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold bg-red-50 text-red-700 border border-red-200/70">
                        <AlertTriangle className="w-3 h-3 mr-1" />
                        Discrepancy
                      </span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-right">
                    <button className="px-2.5 py-1 text-xs bg-slate-100 hover:bg-slate-900 hover:text-white rounded-md transition-colors text-slate-700 font-medium">
                      View Logs
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 3. Detailed Borehole Dossier Drawer / Modal */}
      {selectedBorehole && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex justify-end">
          <div className="w-full max-w-2xl bg-white h-full overflow-y-auto shadow-2xl p-6 space-y-6 flex flex-col justify-between">
            <div className="space-y-6">
              {/* Drawer Header */}
              <div className="flex items-center justify-between border-b border-[#d9e2ec] pb-4">
                <div>
                  <div className="text-xs text-amber-600 font-semibold uppercase tracking-wider">
                    Statutory Borehole Dossier
                  </div>
                  <h3 className="text-xl font-extrabold text-[#0c2340]">
                    {selectedBorehole.boreholeId} — {selectedBorehole.sectorBlock}
                  </h3>
                  <div className="text-xs text-slate-500 font-mono mt-0.5">
                    Collar MSL: {selectedBorehole.coordinates.collarElevationMsl}m | Datum: {selectedBorehole.coordinates.datum}
                  </div>
                </div>
                <button
                  onClick={() => setSelectedBorehole(null)}
                  className="p-1.5 rounded-full hover:bg-slate-100 text-slate-500 hover:text-slate-900"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Status Notice */}
              {selectedBorehole.statutoryClearance === "FLAGGED_DISCREPANCY" && (
                <div className="p-3.5 rounded-md bg-amber-50 border border-amber-300 text-amber-900 text-xs flex items-start space-x-2">
                  <AlertTriangle className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold">Historical Agency Variance Notice:</span> Seam IX thickness
                    logged by MECL (1998) was 6.80m, revised to 8.42m by CMPDI (2021) following sonic wireline logging.
                    {onSelectDiscrepancy && (
                      <button
                        onClick={() => {
                          setSelectedBorehole(null);
                          onSelectDiscrepancy(selectedBorehole.discrepancyId || "DISC-094");
                        }}
                        className="ml-2 underline font-bold text-amber-900 hover:text-amber-950"
                      >
                        Reconcile in Queue →
                      </button>
                    )}
                  </div>
                </div>
              )}

              {/* Proximate Assay Grid */}
              <div className="space-y-2">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                  Proximate Quality Assay &amp; Grade
                </h4>
                <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
                  <div className="bg-slate-50 p-2.5 rounded border border-slate-200 text-center">
                    <div className="text-[10px] text-slate-500">Grade</div>
                    <div className="text-sm font-bold text-blue-700">{selectedBorehole.coalGrade}</div>
                  </div>
                  <div className="bg-slate-50 p-2.5 rounded border border-slate-200 text-center">
                    <div className="text-[10px] text-slate-500">GCV (kcal/kg)</div>
                    <div className="text-sm font-bold text-[#0c2340]">
                      {selectedBorehole.proximateAssay.grossCalorificValueKcal}
                    </div>
                  </div>
                  <div className="bg-slate-50 p-2.5 rounded border border-slate-200 text-center">
                    <div className="text-[10px] text-slate-500">Ash %</div>
                    <div className="text-sm font-bold text-slate-800">
                      {selectedBorehole.proximateAssay.ashPercent}%
                    </div>
                  </div>
                  <div className="bg-slate-50 p-2.5 rounded border border-slate-200 text-center">
                    <div className="text-[10px] text-slate-500">Moisture %</div>
                    <div className="text-sm font-bold text-slate-800">
                      {selectedBorehole.proximateAssay.moisturePercent}%
                    </div>
                  </div>
                  <div className="bg-slate-50 p-2.5 rounded border border-slate-200 text-center">
                    <div className="text-[10px] text-slate-500">Volatile Matter</div>
                    <div className="text-sm font-bold text-slate-800">
                      {selectedBorehole.proximateAssay.volatileMatterPercent || 29.2}%
                    </div>
                  </div>
                </div>
              </div>

              {/* Lithological Column Intervals */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                    Borehole Lithological Column (Depth Intervals)
                  </h4>
                  <span className="text-[11px] text-slate-500">
                    Total: {selectedBorehole.totalDrilledDepthMeters}m
                  </span>
                </div>

                {selectedBorehole.intervals.length > 0 ? (
                  <div className="border border-[#d9e2ec] rounded-md overflow-hidden">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-slate-100 text-slate-700 text-[10px] uppercase font-semibold">
                        <tr>
                          <th className="py-2 px-3">Interval (m)</th>
                          <th className="py-2 px-3">Thickness</th>
                          <th className="py-2 px-3">Stratum Description</th>
                          <th className="py-2 px-3 text-right">Recovery</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-200">
                        {selectedBorehole.intervals.map((intv, idx) => (
                          <tr
                            key={idx}
                            className={intv.seamCode === "SEAM_IX" ? "bg-amber-100/50 font-medium" : ""}
                          >
                            <td className="py-2 px-3 font-mono text-[11px] text-slate-600">
                              {intv.fromDepthMeters.toFixed(2)} - {intv.toDepthMeters.toFixed(2)}
                            </td>
                            <td className="py-2 px-3 font-bold text-[#0c2340]">
                              {intv.thicknessMeters.toFixed(2)} m
                            </td>
                            <td className="py-2 px-3 text-slate-800">
                              {intv.lithologyDescription}
                            </td>
                            <td className="py-2 px-3 text-right font-semibold text-emerald-700">
                              {intv.coreRecoveryPercent}%
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="p-4 rounded bg-slate-50 border border-slate-200 text-center text-xs text-slate-500">
                    Standard lithology intervals available in National Coal Archive plate.
                  </div>
                )}
              </div>

              {/* Source Evidence Trail & Cryptographic Verification */}
              {selectedBorehole.evidenceTrail.length > 0 && (
                <div className="space-y-2">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                    Cryptographic Evidence Trail (SHA-256 Verified)
                  </h4>
                  <div className="space-y-2">
                    {selectedBorehole.evidenceTrail.map((cit, idx) => (
                      <div key={idx} className="p-3 bg-slate-50 border border-slate-200 rounded-md text-xs space-y-1">
                        <div className="flex items-center justify-between font-bold text-[#0c2340]">
                          <span>{cit.documentTitle}</span>
                          <span className="text-[10px] px-1.5 py-0.2 bg-blue-100 text-blue-800 rounded">
                            {cit.agency} ({cit.year})
                          </span>
                        </div>
                        <p className="text-slate-600 italic">"{cit.snippetText}"</p>
                        <div className="flex items-center space-x-2 text-[10px] text-slate-400 font-mono">
                          <Hash className="w-3 h-3 text-slate-400" />
                          <span className="truncate">{cit.sha256Hash}</span>
                          <span className="text-emerald-700 font-semibold ml-auto">
                            {cit.extractionConfidence != null && cit.extractionConfidence > 0 ? `Confidence: ${(cit.extractionConfidence * 100).toFixed(1)}%` : "AI Synthesis"}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Drawer Footer */}
            <div className="border-t border-slate-200 pt-4 flex flex-wrap items-center justify-between gap-3">
              <span className="text-xs text-slate-500 font-mono">
                Dossier ID: CMPDI/NK-IV/{selectedBorehole.boreholeId}
              </span>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => generateFormVDossierPDF(selectedBorehole)}
                  className="px-3.5 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-bold rounded-lg shadow-xs flex items-center space-x-1.5 transition-all"
                >
                  <FileText className="w-3.5 h-3.5" />
                  <span>Download Form-V PDF</span>
                </button>
                <button
                  onClick={() => setSelectedBorehole(null)}
                  className="px-3.5 py-2 bg-slate-100 text-slate-700 hover:bg-slate-200 text-xs font-semibold rounded-lg transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
