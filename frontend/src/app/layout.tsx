import type { Metadata } from "next";
import React from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: "GeoMine AI | Geological & Mining Decision Intelligence",
  description:
    "AI-powered Geological, Mining, and Reporting Solution for CMPDI / Coal India Limited (SIH26023)",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#f8fafc] text-slate-900 antialiased font-sans">
        {children}
      </body>
    </html>
  );
}
