"use client";

import React from "react";
import { 
  Database, 
  Download, 
  ShieldCheck, 
  Printer
} from "lucide-react";
import { BoreholeRecord } from "@/types/geological";
import { generateFormVDossierPDF, generateAllBoreholesRegisterPDF } from "@/utils/pdfGenerator";

interface NationalRepositoryViewProps {
  boreholes?: BoreholeRecord[];
}

export const NationalRepositoryView: React.FC<NationalRepositoryViewProps> = ({ boreholes = [] }) => {
  const sampleBoreholeBH094: BoreholeRecord = {
    boreholeId: "BH-NK-094",
    coalfield: "North Karanpura",
    sectorBlock: "Block IV (Tandwa Sector)",
    coordinates: {
      latitude: "23° 48' 12.4\" N",
      longitude: "85° 08' 45.1\" E",
      collarElevationMsl: 482.35,
      datum: "WGS84 / UTM Zone 45N",
    },
    totalDrilledDepthMeters: 198.50,
    targetSeamThickness: 8.42,
    coalGrade: "G7",
    proximateAssay: {
      ashPercent: 23.4,
      moisturePercent: 6.8,
      volatileMatterPercent: 29.2,
      fixedCarbonPercent: 40.6,
      grossCalorificValueKcal: 5420.0,
    },
    statutoryClearance: "DGMS_CLEARED",
    intervals: [
      {
        fromDepthMeters: 0.0,
        toDepthMeters: 42.10,
        thicknessMeters: 42.10,
        lithologyDescription: "Alluvium and weathered zone",
        coreRecoveryPercent: 62.5,
        seamCode: "ALLUVIUM",
      },
      {
        fromDepthMeters: 42.10,
        toDepthMeters: 114.28,
        thicknessMeters: 72.18,
        lithologyDescription: "Medium Barakar sandstone with shaly streaks",
        coreRecoveryPercent: 88.4,
        seamCode: "SANDSTONE",
      },
      {
        fromDepthMeters: 114.28,
        toDepthMeters: 122.70,
        thicknessMeters: 8.42,
        lithologyDescription: "Target Coal Seam IX: Dull to bright banded coal",
        coreRecoveryPercent: 96.8,
        seamCode: "SEAM_IX",
      },
      {
        fromDepthMeters: 122.70,
        toDepthMeters: 154.10,
        thicknessMeters: 31.40,
        lithologyDescription: "Interburden: Hard siliceous shale and fine sandstone",
        coreRecoveryPercent: 92.1,
        seamCode: "INTERBURDEN",
      },
    ],
    evidenceTrail: [
      {
        documentId: "CMPDI-GR-2021-NK4",
        documentTitle: "CMPDI Detailed Geological Assessment Report — Block IV",
        agency: "CMPDI",
        year: 2021,
        sha256Hash: "9f83c1b894101e4a32e18502f9c45a7d6e1b38a716bf6718d098e7235a90e311",
        extractionConfidence: 0.984,
        snippetText: "Seam IX intercepted at 114.28m, verified clean thickness 8.42m.",
      },
    ],
  };

  const sampleBoreholeBH091: BoreholeRecord = {
    boreholeId: "BH-NK-091",
    coalfield: "North Karanpura",
    sectorBlock: "Block IV (Tandwa Sector)",
    coordinates: {
      latitude: "23° 48' 04.1\" N",
      longitude: "85° 08' 22.8\" E",
      collarElevationMsl: 478.10,
      datum: "WGS84 / UTM Zone 45N",
    },
    totalDrilledDepthMeters: 182.00,
    targetSeamThickness: 7.95,
    coalGrade: "G7",
    proximateAssay: {
      ashPercent: 24.1,
      moisturePercent: 6.5,
      grossCalorificValueKcal: 5380.0,
    },
    statutoryClearance: "DGMS_CLEARED",
    intervals: [
      {
        fromDepthMeters: 0.0,
        toDepthMeters: 38.5,
        thicknessMeters: 38.5,
        lithologyDescription: "Alluvium & topsoil",
        coreRecoveryPercent: 60.0,
        seamCode: "ALLUVIUM",
      },
      {
        fromDepthMeters: 38.5,
        toDepthMeters: 118.2,
        thicknessMeters: 79.7,
        lithologyDescription: "Barakar Sandstone coarse-grained",
        coreRecoveryPercent: 89.0,
        seamCode: "SANDSTONE",
      },
      {
        fromDepthMeters: 118.2,
        toDepthMeters: 126.15,
        thicknessMeters: 7.95,
        lithologyDescription: "Coal Seam IX dull banded",
        coreRecoveryPercent: 95.5,
        seamCode: "SEAM_IX",
      },
    ],
    evidenceTrail: [],
  };

  const registers = [
    {
      id: "FORM-V-NK-094",
      title: "Statutory Form-V Exploration Register: BH-NK-094",
      regulation: "Coal Mines Regulations (CMR) 2017 — Reg. 113",
      issuedBy: "CMPDI Regional Institute II, Ranchi",
      date: "14-Oct-2021",
      clearanceStatus: "DGMS_CLEARED",
      docketNo: "SEC-IV/2025/OK/094",
      boreholeData: sampleBoreholeBH094,
    },
    {
      id: "FORM-V-NK-091",
      title: "Statutory Form-V Exploration Register: BH-NK-091",
      regulation: "Coal Mines Regulations (CMR) 2017 — Reg. 113",
      issuedBy: "CMPDI Regional Institute II, Ranchi",
      date: "10-Sep-2021",
      clearanceStatus: "DGMS_CLEARED",
      docketNo: "SEC-IV/2025/OK/091",
      boreholeData: sampleBoreholeBH091,
    },
    {
      id: "UNFC-111-BLOCK-IV",
      title: "UNFC 111 Proved Geological Reserves Statement — Block IV",
      regulation: "United Nations Framework Classification (111 Proved)",
      issuedBy: "Ministry of Coal / CMPDI Headquarters",
      date: "02-Jan-2026",
      clearanceStatus: "DGMS_CLEARED",
      docketNo: "MOC/UNFC/NK-IV/2026",
      boreholeData: sampleBoreholeBH094,
    },
  ];

  const handleBatchExport = () => {
    const records = boreholes.length > 0 ? boreholes : [sampleBoreholeBH094, sampleBoreholeBH091];
    generateAllBoreholesRegisterPDF(records);
  };

  return (
    <div className="space-y-6">
      {/* 1. Header Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2.5">
            <Database className="w-5 h-5 text-[#121417]" />
            <h2 className="font-bold text-base text-[#121417]">
              National Data Repository (Form-V &amp; DGMS Safety Archive)
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Statutory exploration registers, CMR 2017 Regulation 113 clearances, and UNFC 111 reserve categorization
          </p>
        </div>

        <button 
          onClick={handleBatchExport}
          className="px-3.5 py-2 bg-[#121417] hover:bg-[#181b20] text-white text-xs font-bold rounded-lg shadow-sm flex items-center space-x-2 transition-colors"
        >
          <Printer className="w-4 h-4 text-amber-400" />
          <span>Batch Download All Form-V PDF Registers</span>
        </button>
      </div>

      {/* 2. Repository Registers Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#121417] text-white uppercase text-[11px] font-semibold tracking-wider">
              <tr>
                <th className="py-3 px-4">Register Title</th>
                <th className="py-3 px-4">Statutory Clause</th>
                <th className="py-3 px-4">Certifying Authority</th>
                <th className="py-3 px-4">Docket Number</th>
                <th className="py-3 px-4">Clearance Status</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200/80">
              {registers.map((reg) => (
                <tr key={reg.id} className="hover:bg-slate-50 transition-colors">
                  <td className="py-3 px-4">
                    <div className="font-bold text-slate-900">{reg.title}</div>
                    <div className="text-[10px] text-slate-400 font-mono mt-0.5">ID: {reg.id}</div>
                  </td>
                  <td className="py-3 px-4 text-slate-700 font-medium">{reg.regulation}</td>
                  <td className="py-3 px-4 text-slate-600">{reg.issuedBy}</td>
                  <td className="py-3 px-4 font-mono text-[11px] text-slate-800">{reg.docketNo}</td>
                  <td className="py-3 px-4">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
                      <ShieldCheck className="w-3 h-3 mr-1" />
                      DGMS Cleared
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right space-x-2">
                    <button 
                      onClick={() => generateFormVDossierPDF(reg.boreholeData)}
                      className="px-3 py-1.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold rounded-lg transition-all shadow-xs inline-flex items-center space-x-1.5"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>Download Form-V PDF</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

