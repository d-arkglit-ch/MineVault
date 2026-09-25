"use client";

import React, { useState } from "react";
import { ShieldCheck, Menu } from "lucide-react";

interface TopBarProps {
  activeTabTitle: string;
  language: "EN" | "HI";
  setLanguage: (lang: "EN" | "HI") => void;
  onToggleMobileSidebar: () => void;
}

export const TopBar: React.FC<TopBarProps> = ({
  activeTabTitle,
  language,
  setLanguage,
  onToggleMobileSidebar,
}) => {
  const [fontSize, setFontSize] = useState<"sm" | "md" | "lg">("md");

  const handleFontSizeChange = (size: "sm" | "md" | "lg") => {
    setFontSize(size);
    if (typeof document !== "undefined") {
      document.body.className = `font-size-${size}`;
    }
  };

  return (
    <header className="w-full bg-white border-b border-slate-200 sticky top-0 z-20 shadow-xs">
      {/* 1. Government of India Tricolor Top Bar */}
      <div className="gov-tricolor-stripe w-full" />

      {/* 2. Main Top Utility Bar */}
      <div className="px-3 sm:px-6 md:px-8 py-2.5 flex items-center justify-between gap-2 bg-white">
        {/* Left: Mobile Hamburger Menu & Active Title */}
        <div className="flex items-center space-x-2.5 sm:space-x-3 overflow-hidden">
          {/* Hamburger Menu button - visible only on phones & small screens below md breakpoint */}
          <button
            onClick={onToggleMobileSidebar}
            className="md:hidden p-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-800 border border-slate-200 flex-shrink-0"
            aria-label="Open Navigation Menu"
          >
            <Menu className="w-5 h-5" />
          </button>

          <div className="flex items-center space-x-2 truncate">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse flex-shrink-0" />
            <span className="text-xs sm:text-sm font-bold text-slate-900 tracking-wide truncate">
              {activeTabTitle}
            </span>
          </div>

          <span className="text-slate-300 hidden lg:inline">|</span>
          <span className="text-xs text-slate-500 hidden lg:inline truncate">
            {language === "EN" ? "Government of India • Ministry of Coal" : "भारत सरकार • कोयला मंत्रालय"}
          </span>
        </div>

        {/* Right Accessibility & Language Controls */}
        <div className="flex items-center space-x-2 sm:space-x-3 flex-shrink-0">
          {/* Text Size Accessibility Controls */}
          <div className="hidden xs:flex items-center space-x-1 bg-slate-100 px-1.5 sm:px-2 py-0.5 rounded-md border border-slate-200">
            <span className="text-[10px] text-slate-500 mr-1 font-medium hidden sm:inline">Text:</span>
            <button
              onClick={() => handleFontSizeChange("sm")}
              className={`px-1.5 py-0.5 rounded text-xs font-semibold transition-colors ${
                fontSize === "sm" ? "text-slate-900 bg-white shadow-xs" : "text-slate-600 hover:text-slate-900"
              }`}
              title="Decrease text size"
            >
              A-
            </button>
            <button
              onClick={() => handleFontSizeChange("md")}
              className={`px-1.5 py-0.5 rounded text-xs font-semibold transition-colors ${
                fontSize === "md" ? "text-slate-900 bg-white shadow-xs" : "text-slate-600 hover:text-slate-900"
              }`}
              title="Default text size"
            >
              A
            </button>
            <button
              onClick={() => handleFontSizeChange("lg")}
              className={`px-1.5 py-0.5 rounded text-xs font-semibold transition-colors ${
                fontSize === "lg" ? "text-slate-900 bg-white shadow-xs" : "text-slate-600 hover:text-slate-900"
              }`}
              title="Increase text size"
            >
              A+
            </button>
          </div>

          {/* Bilingual Toggle */}
          <button
            onClick={() => setLanguage(language === "EN" ? "HI" : "EN")}
            className="text-xs text-slate-800 hover:text-slate-950 font-semibold px-2 sm:px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 transition-colors"
          >
            {language === "EN" ? "हिन्दी" : "English"}
          </button>

          {/* NIC / GIGW Standard Tag */}
          <div className="hidden sm:flex items-center space-x-1.5 text-[11px] text-emerald-700 font-semibold bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>NIC Certified</span>
          </div>
        </div>
      </div>
    </header>
  );
};
