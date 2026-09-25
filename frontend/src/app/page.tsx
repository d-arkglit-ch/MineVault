"use client";

import React, { useState, useEffect } from "react";
import { Sidebar } from "@/components/navigation/Sidebar";
import { TopBar } from "@/components/navigation/TopBar";
import { DashboardView } from "@/components/dashboard/DashboardView";
import { BoreholeDirectoryView } from "@/components/boreholes/BoreholeDirectoryView";
import { ExplorationMapView } from "@/components/maps/ExplorationMapView";
import { ReportStudioView } from "@/components/reports/ReportStudioView";
import { VerificationQueueView } from "@/components/verification/VerificationQueueView";
import { NationalRepositoryView } from "@/components/repository/NationalRepositoryView";
import { IngestionDeskModal } from "@/components/ingestion/IngestionDeskModal";
import { BoreholeRecord, DiscrepancyItem } from "@/types/geological";

// Fallback initial dataset matching backend seed_data.py
const INITIAL_BOREHOLES: BoreholeRecord[] = [
  {
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
    statutoryClearance: "FLAGGED_DISCREPANCY",
    discrepancyId: "DISC-094",
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
  },
  {
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
    intervals: [],
    evidenceTrail: [],
  },
  {
    boreholeId: "BH-NK-092",
    coalfield: "North Karanpura",
    sectorBlock: "Block IV (Tandwa Sector)",
    coordinates: {
      latitude: "23° 48' 08.9\" N",
      longitude: "85° 08' 31.4\" E",
      collarElevationMsl: 479.80,
      datum: "WGS84 / UTM Zone 45N",
    },
    totalDrilledDepthMeters: 190.50,
    targetSeamThickness: 8.10,
    coalGrade: "G7",
    proximateAssay: {
      ashPercent: 23.8,
      moisturePercent: 6.9,
      grossCalorificValueKcal: 5410.0,
    },
    statutoryClearance: "DGMS_CLEARED",
    intervals: [],
    evidenceTrail: [],
  },
  {
    boreholeId: "BH-NK-095",
    coalfield: "North Karanpura",
    sectorBlock: "Block IV (Tandwa Sector)",
    coordinates: {
      latitude: "23° 48' 19.3\" N",
      longitude: "85° 09' 02.1\" E",
      collarElevationMsl: 485.60,
      datum: "WGS84 / UTM Zone 45N",
    },
    totalDrilledDepthMeters: 205.00,
    targetSeamThickness: 8.65,
    coalGrade: "G7",
    proximateAssay: {
      ashPercent: 25.2,
      moisturePercent: 7.1,
      grossCalorificValueKcal: 5240.0,
    },
    statutoryClearance: "DGMS_CLEARED",
    intervals: [],
    evidenceTrail: [],
  },
];

const INITIAL_DISCREPANCIES: DiscrepancyItem[] = [
  {
    discrepancyId: "DISC-094",
    boreholeId: "BH-NK-094",
    coalfield: "North Karanpura",
    block: "Block IV (Tandwa)",
    seam: "Seam IX",
    agencyA: "MECL",
    surveyYearA: 1998,
    reportedThicknessA: 6.80,
    methodA: "Rotary Core Drilling (68% recovery, mud-flush)",
    agencyB: "CMPDI",
    surveyYearB: 2021,
    reportedThicknessB: 8.42,
    methodB: "Digital Sonic Wireline Log & High-Recovery Core (96.8%)",
    thicknessDeltaMeters: 1.62,
    status: "UNDER_REVIEW",
    reconciliationNotes:
      "Historical MECL 1998 survey under-reported thickness due to core washout. CMPDI 2021 sonic caliper logs confirm 8.42m true thickness (+5.44 MT proved reserve impact).",
    digitalSignatureHash: "f4c324147c0353070c48a311b9a26c78309f2d63bfd9c1abc54864ae1427c96e",
    auditDocketNo: "CMPDI/RI-II/NK-IV/DISC-094/2026",
  },
];

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<string>("dashboard");
  const [isIngestionModalOpen, setIsIngestionModalOpen] = useState(false);
  const [boreholes, setBoreholes] = useState<BoreholeRecord[]>(INITIAL_BOREHOLES);
  const [discrepancies, setDiscrepancies] = useState<DiscrepancyItem[]>(INITIAL_DISCREPANCIES);

  // Fetch from FastAPI backend if active
  useEffect(() => {
    async function loadData() {
      try {
        const bhRes = await fetch("http://localhost:8000/api/v1/boreholes/");
        if (bhRes.ok) {
          const data = await bhRes.json();
          setBoreholes(data);
        }
      } catch {
        // use seeded fallback
      }

      try {
        const discRes = await fetch("http://localhost:8000/api/v1/discrepancies/");
        if (discRes.ok) {
          const data = await discRes.json();
          setDiscrepancies(data);
        }
      } catch {
        // use seeded fallback
      }
    }
    loadData();
  }, []);

  const handleApproveDiscrepancy = (id: string) => {
    setDiscrepancies((prev) =>
      prev.map((d) => (d.discrepancyId === id ? { ...d, status: "RESOLVED" } : d))
    );
    setBoreholes((prev) =>
      prev.map((b) =>
        b.discrepancyId === id ? { ...b, statutoryClearance: "DGMS_CLEARED" } : b
      )
    );
  };

  const handleIngestNewBorehole = (record: BoreholeRecord) => {
    setBoreholes((prev) => {
      const idx = prev.findIndex((b) => b.boreholeId === record.boreholeId);
      if (idx >= 0) {
        const copy = [...prev];
        copy[idx] = record;
        return copy;
      }
      return [record, ...prev];
    });
  };

  const pendingDiscrepancies = discrepancies.filter((d) => d.status === "UNDER_REVIEW").length;

  const [language, setLanguage] = useState<"EN" | "HI">("EN");
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  const tabTitles: Record<string, string> = {
    dashboard: language === "EN" ? "1. Executive Dashboard & National Overview" : "१. कार्यकारी डैशबोर्ड",
    boreholes: language === "EN" ? "2. Sector Borehole Directory & Drill Logs" : "२. सेक्टर बोरहोल निर्देशिका",
    maps: language === "EN" ? "3. Block Exploration Maps & Stratigraphic Cross-Section" : "३. ब्लॉक अन्वेषण मानचित्र",
    reports: language === "EN" ? "4. AI Geological Report Studio & PQ Briefs" : "४. भूवैज्ञानिक रिपोर्ट स्टूडियो",
    verification: language === "EN" ? "5. Multi-Agency Verification & Reconciliation Queue" : "५. सत्यापन और समाधान कतार",
    repository: language === "EN" ? "6. National Data Repository & Form-V Archive" : "६. राष्ट्रीय डेटा भंडार",
  };

  return (
    <div className="min-h-screen flex bg-[#f3f4f6] text-slate-900 font-sans antialiased">
      {/* 1. LEFT SECTION: Responsive Sidebar (Drawer on mobile <md, fixed left column on >=md) */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        openIngestionModal={() => setIsIngestionModalOpen(true)}
        discrepancyCount={pendingDiscrepancies}
        language={language}
        isOpen={isMobileSidebarOpen}
        onClose={() => setIsMobileSidebarOpen(false)}
      />

      {/* 2. RIGHT SECTION: TopBar + Dynamic Main Workspace */}
      <div className="flex-1 flex flex-col min-w-0 min-h-screen">
        <TopBar
          activeTabTitle={tabTitles[activeTab] || "GeoMine Portal"}
          language={language}
          setLanguage={setLanguage}
          onToggleMobileSidebar={() => setIsMobileSidebarOpen((prev) => !prev)}
        />

        {/* Main Workspace Content Area with responsive breakpoint padding */}
        <main className="flex-1 px-3 sm:px-6 md:px-8 py-4 sm:py-6 max-w-7xl w-full mx-auto">
          {activeTab === "dashboard" && (
            <DashboardView onNavigate={(tab) => setActiveTab(tab)} />
          )}
          {activeTab === "boreholes" && (
            <BoreholeDirectoryView
              boreholes={boreholes}
              onSelectDiscrepancy={(id) => {
                setActiveTab("verification");
              }}
            />
          )}
          {activeTab === "maps" && <ExplorationMapView boreholes={boreholes} />}
          {activeTab === "reports" && <ReportStudioView />}
          {activeTab === "verification" && (
            <VerificationQueueView
              discrepancies={discrepancies}
              onApproveSuccess={handleApproveDiscrepancy}
            />
          )}
          {activeTab === "repository" && <NationalRepositoryView boreholes={boreholes} />}
        </main>

        {/* Statutory Government Footer */}
        <footer className="bg-[#09192b] text-slate-400 text-xs py-5 border-t border-slate-800 mt-auto">
          <div className="px-4 sm:px-8 flex flex-wrap items-center justify-between gap-4">
            <div>
              <div className="text-white font-bold text-xs">
                Central Mine Planning &amp; Design Institute Limited (CMPDI)
              </div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                A Subsidiary of Coal India Limited • Ministry of Coal, Government of India
              </div>
            </div>
            <div className="flex items-center space-x-3 text-[11px] text-slate-400">
              <span>GIGW 3.0 Standard</span>
              <span>•</span>
              <span>NIC Certified</span>
              <span>•</span>
              <span>DGMS CMR 2017 Reg. 113 Compliant</span>
            </div>
          </div>
        </footer>
      </div>

      {/* Ingestion & Bounding Box Modal */}
      <IngestionDeskModal
        isOpen={isIngestionModalOpen}
        onClose={() => setIsIngestionModalOpen(false)}
        onIngestSuccess={handleIngestNewBorehole}
      />
    </div>
  );
}
