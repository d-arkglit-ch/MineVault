"use client";

import React from "react";
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
  ChevronRight,
  X
} from "lucide-react";

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  openIngestionModal: () => void;
  discrepancyCount?: number;
  language?: "EN" | "HI";
  isOpen?: boolean;
  onClose?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  activeTab,
  setActiveTab,
  openIngestionModal,
  discrepancyCount = 2,
  language = "EN",
  isOpen = false,
  onClose,
}) => {
  const navItems = [
    { id: "dashboard", label: language === "EN" ? "Dashboard" : "डैशबोर्ड", icon: Activity, number: "1" },
    { id: "boreholes", label: language === "EN" ? "Borehole Directory" : "बोरहोल निर्देशिका", icon: Layers, number: "2" },
    { id: "maps", label: language === "EN" ? "Block Exploration Maps" : "ब्लॉक अन्वेषण मानचित्र", icon: MapPin, number: "3" },
    { id: "reports", label: language === "EN" ? "Geological Reports" : "भूवैज्ञानिक रिपोर्ट", icon: FileText, number: "4" },
    {
      id: "verification",
      label: language === "EN" ? "Verification Queue" : "सत्यापन कतार",
      icon: CheckCircle2,
      badge: discrepancyCount,
      number: "5"
    },
    { id: "repository", label: language === "EN" ? "National Data Repository" : "राष्ट्रीय डेटा भंडार", icon: Database, number: "6" },
  ];

  const handleNavClick = (tabId: string) => {
    setActiveTab(tabId);
    if (onClose) onClose();
  };

  return (
    <>
      {/* 1. Mobile Backdrop Overlay (below md breakpoint) */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 bg-black/70 backdrop-blur-xs z-40 md:hidden transition-opacity"
          aria-hidden="true"
        />
      )}

      {/* 2. Responsive Sidebar (Drawer on mobile <md, fixed left column on >=md) */}
      <aside
        className={`fixed md:sticky top-0 left-0 z-50 md:z-30 w-72 bg-[#121417] text-slate-100 flex flex-col flex-shrink-0 h-screen border-r border-[#22272e] select-none transition-transform duration-300 ease-in-out ${isOpen ? "translate-x-0 shadow-2xl" : "-translate-x-full md:translate-x-0"
          }`}
      >
        {/* Header: Official Government & CMPDI Branding */}
        <div className="p-4 border-b border-[#22272e] bg-[#0c0e11] flex items-center justify-between">
          <div className="flex items-center space-x-3 overflow-hidden">
            {/* Ashoka Emblem Insignia */}
            <div className="w-10 h-10 bg-white rounded-lg p-1 flex items-center justify-center border border-amber-500/40 shadow-sm flex-shrink-0">
              <div className="text-center font-serif text-[#121417] leading-none">
                <span className="text-[7px] font-bold block tracking-tighter">Mine</span>
                <span className="text-[10px] font-extrabold block">Vault</span>
              </div>
            </div>

            <div className="overflow-hidden">
              <div className="flex items-center space-x-1.5">
                <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400 truncate">
                  CMPDI / CIL
                </span>
                <span className="text-[9px] px-1 py-0.2 bg-amber-500/20 text-amber-300 border border-amber-500/30 rounded font-mono">
                  SIH26023
                </span>
              </div>
              <h1 className="text-sm font-bold tracking-tight text-white leading-snug truncate mt-0.5">
                MineVault
              </h1>
              <p className="text-[10px] text-slate-400 truncate">
                National Coal Records Portal
              </p>
            </div>
          </div>

          {/* Close button for mobile phones */}
          <button
            onClick={onClose}
            className="md:hidden p-1.5 text-slate-400 hover:text-white rounded-lg bg-[#181b20] border border-[#262c36]"
            aria-label="Close Navigation"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Primary Action: Ingestion Desk (OCR) Trigger */}
        <div className="p-3 border-b border-[#22272e]">
          <button
            onClick={() => {
              openIngestionModal();
              if (onClose) onClose();
            }}
            className="w-full flex items-center justify-center space-x-2 py-2.5 px-3 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs rounded-lg shadow-sm transition-all hover:shadow"
          >
            <UploadCloud className="w-4 h-4" />
            <span>Ingestion Desk (OCR)</span>
          </button>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 p-3 space-y-1.5 overflow-y-auto">
          <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider px-2 py-1">
            Navigation Modules
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`w-full flex items-center justify-between px-3 py-2.5 text-xs font-medium rounded-lg transition-all text-left ${isActive
                  ? "bg-[#1f242c] text-amber-400 font-semibold border-l-2 border-amber-400 shadow-xs"
                  : "text-slate-300 hover:text-white hover:bg-[#181b20]"
                  }`}
              >
                <div className="flex items-center space-x-2.5 truncate">
                  <Icon className={`w-4 h-4 flex-shrink-0 ${isActive ? "text-amber-400" : "text-slate-400"}`} />
                  <span className="truncate">{item.number}. {item.label}</span>
                </div>

                {item.badge !== undefined && item.badge > 0 ? (
                  <span className="ml-1.5 px-1.5 py-0.2 text-[10px] font-bold rounded-full bg-amber-500 text-slate-950">
                    {item.badge}
                  </span>
                ) : isActive ? (
                  <ChevronRight className="w-3.5 h-3.5 text-amber-400/70" />
                ) : null}
              </button>
            );
          })}
        </nav>

        {/* Authenticated Officer Profile */}
        <div className="p-3 border-t border-[#22272e] bg-[#0c0e11] mt-auto">
          <div className="flex items-center space-x-2.5 bg-[#181b20] p-2.5 rounded-lg border border-[#262c36]">
            <UserCheck className="w-5 h-5 text-emerald-400 flex-shrink-0" />
            <div className="text-left leading-tight truncate">
              <div className="text-xs font-bold text-white truncate">Er. S. Mukhopadhyay</div>
              <div className="text-[10px] text-slate-400 truncate mt-0.5">Chief Geologist | RI-II Ranchi</div>
            </div>
          </div>

          {/* GIGW Compliance Tag */}
          <div className="mt-2.5 flex items-center justify-between px-1 text-[10px] text-slate-400">
            <div className="flex items-center space-x-1 text-emerald-400 font-medium">
              <ShieldCheck className="w-3 h-3" />
              <span>GIGW 3.0 Standard</span>
            </div>
            <span className="text-slate-500">DGMS CMR 2017</span>
          </div>
        </div>
      </aside>
    </>
  );
};
