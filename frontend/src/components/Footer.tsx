import React from 'react';
import { Database, ShieldCheck, Heart } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-slate-200 mt-16 py-8 text-xs text-slate-500">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pb-6 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2 text-slate-800 font-semibold mb-2">
              <Database className="w-4 h-4 text-sky-600" />
              <span>Genuine Empirical Data</span>
            </div>
            <p className="text-slate-500 leading-relaxed">
              Air quality records collected by CPCB & KSPCB via the XKDR Forum CAAQM API. Meteorological reanalysis provided by ECMWF ERA5 via Open-Meteo. Zero synthetic records.
            </p>
          </div>

          <div>
            <div className="flex items-center gap-2 text-slate-800 font-semibold mb-2">
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>Scientific Rigor & CPCB Compliance</span>
            </div>
            <p className="text-slate-500 leading-relaxed">
              Calculated using official CPCB 2014 Table 3.2 piecewise linear interpolation for categories 1–5, an explicit 500 ceiling cap project policy for Severe values, and a 16-hour sufficiency threshold.
            </p>
          </div>

          <div>
            <div className="flex items-center gap-2 text-slate-800 font-semibold mb-2">
              <Heart className="w-4 h-4 text-rose-500" />
              <span>Hackathon Integrity</span>
            </div>
            <p className="text-slate-500 leading-relaxed">
              Built for the Data Science Hackathon. 100% offline-first demonstration architecture with zero external runtime dependencies on localhost.
            </p>
          </div>
        </div>

        <div className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-slate-400">
          <div>
            © 2026 BreatheWise — Bengaluru Air Quality & Weather Intelligence. Government Open Data License (GODL) / CC-BY 4.0.
          </div>
          <div className="font-mono text-[11px]">
            Artifact: v1.2.0 • 670 Historical Calendar Days • 14 Stations
          </div>
        </div>
      </div>
    </footer>
  );
};
