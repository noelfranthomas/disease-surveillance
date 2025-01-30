"use client";

import { useState } from "react";
import { MpoxMap } from "@/components/Map";
import { FloatingPanel } from "@/components/FloatingPanel";
import {
  TimeSeriesChart,
  MonthlyBarChart,
  RegionalPieChart,
} from "@/components/Chart";
import { Input } from "@/components/ui/input";

export default function Page() {
  const mpoxCases = [
    { lat: 40.7128, lng: -74.006, count: 100 }, // e.g. US
    { lat: 51.5074, lng: -0.1278, count: 200 }, // e.g. UK
    { lat: 35.6895, lng: 139.6917, count: 50 }, // e.g. Japan
  ];

  // Suppose these countries have mpox data. Use ISO Alpha-3 codes:
  // US: USA, UK: GBR, Japan: JPN
  const countriesWithMpoxData = ["USA", "GBR", "COD"];

  const [search, setSearch] = useState("");
  const [isFocused, setIsFocused] = useState(false);

  const suggestions = [
    "Statistics in Region A",
    "Outbreak hotspots",
    "Compare 2023 vs 2024",
  ];
  const filteredSuggestions = suggestions.filter((s) =>
    s.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <div className="relative w-full h-screen">
      <MpoxMap cases={mpoxCases} countriesWithData={countriesWithMpoxData} />

      {/* Global Overview Panel (Top-Left) */}
      <div className="absolute top-4 left-4 w-64">
        <FloatingPanel title="Global Mpox Overview">
          <p className="text-sm">Total Cases: 380</p>
          <p className="text-sm">Total Deaths: 5</p>
          <p className="text-sm">Last Update: 2024-01-07</p>
        </FloatingPanel>
      </div>

      {/* Charts Panel (Right Side) */}
      <div className="absolute top-4 right-4 bottom-4">
        <FloatingPanel
          title="Mpox Data Insights"
          className="h-full flex flex-col"
        >
          <div className="bg-white/80 rounded-lg p-2 mb-6">
            <h3 className="text-sm font-semibold mb-2">
              Daily Cases Over Time
            </h3>
            <TimeSeriesChart
              chartProps={{
                margin: { top: 20, right: 20, bottom: 20, left: 20 },
              }}
            />
            <p className="text-xs text-gray-600 mt-2">
              Shows daily mpox cases for the selected period.
            </p>
          </div>

          <div className="bg-white/80 rounded-lg p-2">
            <h3 className="text-sm font-semibold mb-2">
              Monthly Case Distribution
            </h3>
            <MonthlyBarChart
              chartProps={{
                margin: { top: 20, right: 20, bottom: 20, left: 20 },
              }}
            />
            <p className="text-xs text-gray-600 mt-2">
              Compare total cases month-over-month.
            </p>
          </div>
        </FloatingPanel>
      </div>

      {/* Search box at bottom center */}
      <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 w-96 backdrop-blur-md bg-white/70 shadow-xl rounded-full">
        <div className="relative">
          <Input
            placeholder="Ask the mpox chatbot..."
            className="rounded-full"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => {
              setTimeout(() => setIsFocused(false), 100);
            }}
          />
          {isFocused && filteredSuggestions.length > 0 && (
            <div className="absolute bottom-full mb-2 w-full bg-white shadow-lg rounded-lg z-50 p-2">
              {filteredSuggestions.map((item, idx) => (
                <div
                  key={idx}
                  className="p-2 hover:bg-gray-100 cursor-pointer rounded"
                  onMouseDown={() => {
                    setSearch(item);
                  }}
                >
                  {item}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
