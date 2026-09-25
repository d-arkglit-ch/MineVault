"use client";

import React, { useState } from "react";
import { 
  FileText, 
  Layers, 
  MapPin, 
  CheckCircle2, 
  Database, 
  UploadCloud, 
  ShieldCheck, 
  UserCheck, 
  Activity,
  AlertTriangle
} from "lucide-react";

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  openIngestionModal: () => void;
  discrepancyCount?: number;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  openIngestionModal,
  discrepancyCount = 2,
}) => {
  const [fontSize, setFontSize] = useState<"sm" | "md" | "lg">("md");
  const [language, setLanguage] = useState<"EN" | "HI">("EN");

  const handleFontSizeChange = (size: "sm" | "md" | "lg") => {
    setFontSize(size);
    if (typeof document !== "undefined") {
      document.body.className = `font-size-${size}`;
    }
  };

  const navItems = [
    { id: "dashboard", label: language === "EN" ? "1. Dashboard" : "१. डैशबोर्ड", icon: Activity },
    { id: "boreholes", label: language === "EN" ? "2. Borehole Directory" : "२. बोरहोल निर्देशिका", icon: Layers },
    { id: "maps", label: language === "EN" ? "3. Block Exploration Maps" : "३. ब्लॉक अन्वेषण मानचित्र", icon: MapPin },
    { id: "reports", label: language === "EN" ? "4. Geological Reports" : "४. भूवैज्ञानिक रिपोर्ट", icon: FileText },
    { 
      id: "verification", 
      label: language === "EN" ? "5. Verification Queue" : "५. सत्यापन कतार", 
      icon: CheckCircle2,
      badge: discrepancyCount 
    },
    { id: "repository", label: language === "EN" ? "6. National Data Repository" : "६. राष्ट्रीय डेटा भंडार", icon: Database },
  ];

  return (
    <header className="w-full bg-white border-b border-slate-200 select-none sticky top-0 z-40 shadow-sm">
      {/* 1. Government of India Tricolor Top Bar */}
      <div className="gov-tricolor-stripe w-full" />

      {/* 2. GIGW 3.0 Top Utility Access Bar */}
      <div className="bg-[#09192b] text-slate-300 text-xs py-1.5 px-4 sm:px-8 flex flex-wrap items-center justify-between border-b border-slate-800/80">
        <div className="flex items-center space-x-3">
          <span className="font-semibold text-slate-200">
            {language === "EN" ? "भारत सरकार | Government of India" : "भारत सरकार | Government of India"}
          </span>
          <span className="text-slate-600">|</span>
          <span className="hidden md:inline text-slate-400">
            {language === "EN" ? "Ministry of Coal • CMPDI & CIL Subsidiaries" : "कोयला मंत्रालय • सीएमपीडीआई और सीआईएल"}
          </span>
        </div>

        <div className="flex items-center space-x-3">
          {/* Text Size Accessibility Controls */}
          <div className="flex items-center space-x-1 bg-slate-800/90 px-2 py-0.5 rounded border border-slate-700/80">
            <span className="text-[10px] text-slate-400 mr-1">Text:</span>
            <button
              onClick={() => handleFontSizeChange("sm")}
              className={`px-1.5 py-0.5 rounded text-xs font-semibold transition-colors ${fontSize === "sm" ? "text-amber-400 bg-slate-700" : "text-slate-300 hover:text-white"}`}
              title="Decrease text size"
            >
              A-
            </button>
            <button
              onClick={() => handleFontSizeChange("md")}
              className={`px-1.5 py-0.5 rounded text-xs font-semibold transition-colors ${fontSize === "md" ? "text-amber-400 bg-slate-700" : "text-slate-300 hover:text-white"}`}
              title="Default text size"
            >
              A
            </button>
            <button
              onClick={() => handleFontSizeChange("lg")}
              className={`px-1.5 py-0.5 rounded text-xs font-semibold transition-colors ${fontSize === "lg" ? "text-amber-400 bg-slate-700" : "text-slate-300 hover:text-white"}`}
              title="Increase text size"
            >
              A+
            </button>
          </div>

          {/* Bilingual Toggle */}
          <button
            onClick={() => setLanguage(language === "EN" ? "HI" : "EN")}
            className="text-xs text-amber-300 hover:text-amber-200 font-semibold px-2.5 py-0.5 rounded bg-slate-800 border border-slate-700/80 transition-colors"
          >
            {language === "EN" ? "हिन्दी" : "English"}
          </button>

          {/* GIGW 3.0 Standard Badge */}
          <div className="hidden lg:flex items-center space-x-1.5 text-[11px] text-emerald-400 font-medium pl-1">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>GIGW 3.0 Compliant</span>
          </div>
        </div>
      </div>

      {/* 3. Official Ministry & CMPDI Masthead */}
      <div className="bg-[#0f2744] text-white px-4 sm:px-8 py-3.5 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-3.5">
          {/* Ashoka Emblem Emblem / Government Insignia */}
          <div className="w-11 h-11 bg-white rounded-lg p-1 flex items-center justify-center border border-amber-500/20 shadow-sm flex-shrink-0">
            <div className="text-center font-serif text-[#0f2744] leading-none">
              <span className="text-[8px] font-bold block tracking-tighter">सत्यमेव</span>
              <span className="text-[11px] font-extrabold block">जयते</span>
              <span className="text-[7px] text-slate-500 font-sans block mt-0.5 font-bold">GOI</span>
            </div>
          </div>

          <div>
            <div className="flex items-center space-x-2">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-amber-400">
                Coal India Limited / CMPDI
              </span>
              <span className="text-[10px] px-1.5 py-0.2 bg-amber-500/20 text-amber-300 border border-amber-500/30 rounded font-mono font-medium">
                SIH26023
              </span>
            </div>
            <h1 className="text-base sm:text-lg font-bold tracking-tight text-white leading-tight mt-0.5">
              CMPDI Geological Intelligence &amp; Exploration Records Portal
            </h1>
            <p className="text-[11px] text-slate-300 hidden sm:block mt-0.5">
              National Coal Inventory Automation, Source-Traceable AI Workflow &amp; Statutory Dossiers
            </p>
          </div>
        </div>

        {/* Action Controls: Officer Badge & Ingestion Desk Trigger */}
        <div className="flex items-center space-x-3">
          <button
            onClick={openIngestionModal}
            className="flex items-center space-x-2 px-3.5 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-xs rounded-lg shadow-sm transition-all hover:shadow"
          >
            <UploadCloud className="w-4 h-4" />
            <span>Ingestion Desk (OCR)</span>
          </button>

          {/* Authenticated Officer Badge per PRD */}
          <div className="hidden md:flex items-center space-x-2.5 bg-[#09192b]/90 px-3 py-1.5 rounded-lg border border-slate-700/70">
            <UserCheck className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <div className="text-left leading-tight">
              <div className="text-xs font-semibold text-white">Er. S. Mukhopadhyay</div>
              <div className="text-[10px] text-slate-400">Chief Geologist | RI-II Ranchi</div>
            </div>
          </div>
        </div>
      </div>

      {/* 4. Primary Navigation Bar (6 Core Tabs) */}
      <nav className="bg-slate-50 border-b border-slate-200/90 px-4 sm:px-8 overflow-x-auto">
        <div className="flex items-center space-x-1 sm:space-x-1.5 py-1.5 min-w-max">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-2 px-3.5 py-2 text-xs font-medium rounded-md transition-all ${
                  isActive
                    ? "bg-white text-[#0f2744] font-bold shadow-xs border border-slate-200/80"
                    : "text-slate-600 hover:text-[#0f2744] hover:bg-slate-200/60"
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? "text-[#0f2744]" : "text-slate-500"}`} />
                <span>{item.label}</span>
                {item.badge !== undefined && item.badge > 0 && (
                  <span className="ml-1 px-1.5 py-0.2 text-[10px] font-bold rounded-full bg-amber-500 text-slate-950">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </nav>
    </header>
  );
};
