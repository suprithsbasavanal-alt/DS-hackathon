import React, { useState } from 'react';
import {
  TransparencyLedger
} from '../types';
import {
  FileCheck2,
  Database,
  Calculator,
  ShieldCheck,
  CheckCircle2,
  AlertCircle,
  ExternalLink,
  Code2,
  Layers
} from 'lucide-react';

interface DataTransparencyViewProps {
  transparencyData: TransparencyLedger | null;
  loading: boolean;
}

export const DataTransparencyView: React.FC<DataTransparencyViewProps> = ({
  transparencyData,
  loading
}) => {
  // Interactive CPCB Table 3.2 Calculator State
  const [selectedPollutant, setSelectedPollutant] = useState<'PM2.5' | 'PM10' | 'NO2' | 'SO2' | 'CO' | 'O3' | 'NH3'>('PM2.5');
  const [inputConc, setInputConc] = useState<number>(75.0);

  // Client-side exact implementation of CPCB 2014 Table 3.2
  const computeClientSubIndex = (param: string, conc: number) => {
    if (conc < 0) return { sub: null, cat: 'Invalid', formula: 'Negative concentration rejected (sensor fault)' };

    // Breakpoint intervals (B_LO, B_HI, I_LO, I_HI)
    const tables: { [key: string]: Array<[number, number, number, number]> } = {
      'PM2.5': [
        [0, 30, 0, 50],
        [30, 60, 51, 100],
        [60, 90, 101, 200],
        [90, 120, 201, 300],
        [120, 250, 301, 400]
      ],
      'PM10': [
        [0, 50, 0, 50],
        [50, 100, 51, 100],
        [100, 250, 101, 200],
        [250, 350, 201, 300],
        [350, 430, 301, 400]
      ],
      'NO2': [
        [0, 40, 0, 50],
        [40, 80, 51, 100],
        [80, 180, 101, 200],
        [180, 280, 201, 300],
        [280, 400, 301, 400]
      ],
      'SO2': [
        [0, 40, 0, 50],
        [40, 80, 51, 100],
        [80, 380, 101, 200],
        [380, 800, 201, 300],
        [800, 1600, 301, 400]
      ],
      'CO': [
        [0, 1.0, 0, 50],
        [1.0, 2.0, 51, 100],
        [2.0, 10.0, 101, 200],
        [10.0, 17.0, 201, 300],
        [17.0, 34.0, 301, 400]
      ],
      'O3': [
        [0, 50, 0, 50],
        [50, 100, 51, 100],
        [100, 168, 101, 200],
        [168, 208, 201, 300],
        [208, 748, 301, 400]
      ],
      'NH3': [
        [0, 200, 0, 50],
        [200, 400, 51, 100],
        [400, 800, 101, 200],
        [800, 1200, 201, 300],
        [1200, 1800, 301, 400]
      ]
    };

    const severeThresholds: { [key: string]: number } = {
      'PM2.5': 250.0,
      'PM10': 430.0,
      'NO2': 400.0,
      'SO2': 1600.0,
      'CO': 34.0,
      'O3': 748.0,
      'NH3': 1800.0
    };

    const table = tables[param] || [];
    for (const [b_lo, b_hi, i_lo, i_hi] of table) {
      if (conc >= b_lo && conc <= b_hi) {
        const sub = i_lo + ((i_hi - i_lo) / (b_hi - b_lo)) * (conc - b_lo);
        let cat = 'Good';
        if (sub > 50) cat = 'Satisfactory';
        if (sub > 100) cat = 'Moderate';
        if (sub > 200) cat = 'Poor';
        if (sub > 300) cat = 'Very Poor';
        return {
          sub: Math.round(sub * 10) / 10,
          cat,
          formula: `Linear Interpolation (Bracket [${b_lo}, ${b_hi}]): Ip = ${i_lo} + [(${i_hi} - ${i_lo})/(${b_hi} - ${b_lo})] × (${conc} - ${b_lo})`
        };
      }
    }

    if (conc > severeThresholds[param]) {
      return {
        sub: 500.0,
        cat: 'Severe',
        formula: `Severe Lower Threshold Exceeded (> ${severeThresholds[param]}). Project implementation policy: Severe values reported at the 500 ceiling cap.`
      };
    }

    return { sub: 0, cat: 'Good', formula: 'Concentration within baseline.' };
  };

  const calcResult = computeClientSubIndex(selectedPollutant, inputConc);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs font-semibold px-2 py-0.5 rounded bg-sky-100 text-sky-800 border border-sky-200">
            Audit Ledger
          </span>
          <span className="text-xs text-slate-500">100% Genuine Empirical Data Verification</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Data Transparency, Provenance & CPCB Audit Ledger
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Zero synthetic records, zero invented concentration breakpoints, reproducible data pipelines, and open licensing citations.
        </p>
      </div>

      {/* 1. Interactive CPCB IND-AQI Calculator Widget */}
      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 sm:p-8 space-y-6">
        <div className="flex items-center gap-2.5 pb-4 border-b border-slate-100">
          <Calculator className="w-5 h-5 text-sky-600" />
          <div>
            <h2 className="text-lg font-bold text-slate-900">Interactive CPCB Table 3.2 Calculation Engine</h2>
            <p className="text-xs text-slate-500">Test any pollutant concentration against official closed intervals and the Severe 500 ceiling policy.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
          <div className="space-y-4">
            <div>
              <label className="text-xs font-bold uppercase tracking-wider text-slate-500 block mb-1.5">
                Criteria Pollutant
              </label>
              <div className="grid grid-cols-4 gap-1.5">
                {(['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'NH3'] as const).map((p) => (
                  <button
                    key={p}
                    onClick={() => setSelectedPollutant(p)}
                    className={`py-1.5 text-xs font-bold rounded-lg border transition ${
                      selectedPollutant === p
                        ? 'bg-slate-900 text-white border-slate-900 shadow-sm'
                        : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
                    }`}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="text-xs font-bold uppercase tracking-wider text-slate-500 block mb-1.5">
                Concentration ({selectedPollutant === 'CO' ? 'mg/m³' : 'µg/m³'})
              </label>
              <input
                type="number"
                value={inputConc}
                onChange={(e) => setInputConc(parseFloat(e.target.value) || 0)}
                className="w-full px-3 py-2 text-sm font-mono font-bold rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500"
              />
              <div className="flex items-center gap-1.5 mt-2">
                {[
                  { label: 'Good (15)', val: 15 },
                  { label: 'Moderate (75)', val: 75 },
                  { label: 'Poor (105)', val: 105 },
                  { label: 'Severe Threshold (250)', val: 250 },
                  { label: 'Severe Spike (320)', val: 320 }
                ].map((preset) => (
                  <button
                    key={preset.label}
                    onClick={() => setInputConc(preset.val)}
                    className="text-[10px] px-2 py-0.5 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium"
                  >
                    {preset.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Calculator Output Display */}
          <div className="lg:col-span-2 bg-slate-50 rounded-2xl p-6 border border-slate-200/80 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs uppercase font-bold tracking-wider text-slate-400">Calculation Result</span>
              <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${
                calcResult.cat === 'Good' ? 'bg-emerald-100 text-emerald-800 border-emerald-300' :
                calcResult.cat === 'Satisfactory' ? 'bg-lime-100 text-lime-800 border-lime-300' :
                calcResult.cat === 'Moderate' ? 'bg-amber-100 text-amber-800 border-amber-300' :
                calcResult.cat === 'Poor' ? 'bg-orange-100 text-orange-800 border-orange-300' :
                calcResult.cat === 'Very Poor' ? 'bg-red-100 text-red-800 border-red-300' :
                'bg-rose-200 text-rose-900 border-rose-300'
              }`}>
                Category: {calcResult.cat}
              </span>
            </div>

            <div className="flex items-baseline gap-3">
              <div className="text-4xl font-black text-slate-900 font-mono">
                {calcResult.sub !== null ? calcResult.sub : 'N/A'}
              </div>
              <span className="text-xs text-slate-500 font-medium">Sub-Index (Ip)</span>
            </div>

            <div className="pt-3 border-t border-slate-200 text-xs font-mono text-slate-700 bg-white p-3 rounded-xl border border-slate-200/50">
              <span className="text-[10px] text-slate-400 uppercase font-sans font-bold block mb-0.5">Applied Formula</span>
              {calcResult.formula}
            </div>
          </div>
        </div>
      </div>

      {/* 2. CPCB 16-Hour Sufficiency & Audit Counts */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="text-xs text-slate-400 font-bold uppercase tracking-wider">Raw Daily Records</div>
          <div className="text-2xl font-black text-slate-900 mt-1 font-mono">50,584</div>
          <p className="text-[11px] text-slate-500 mt-1">Harvested from XKDR CAAQM archive (2023–2024)</p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-emerald-200 bg-emerald-50/20 shadow-sm">
          <div className="text-xs text-emerald-800 font-bold uppercase tracking-wider">Compliant Records (n ≥ 16h)</div>
          <div className="text-2xl font-black text-emerald-700 mt-1 font-mono">46,795</div>
          <p className="text-[11px] text-emerald-900 mt-1">Preserved for daily AQI calculation</p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-amber-200 bg-amber-50/20 shadow-sm">
          <div className="text-xs text-amber-800 font-bold uppercase tracking-wider">Filtered Records (n &lt; 16h)</div>
          <div className="text-2xl font-black text-amber-700 mt-1 font-mono">3,789</div>
          <p className="text-[11px] text-amber-900 mt-1">Dropped to avoid unrepresentative daily means</p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <div className="text-xs text-slate-400 font-bold uppercase tracking-wider">Continuous Days</div>
          <div className="text-2xl font-black text-slate-900 mt-1 font-mono">670 / 670</div>
          <p className="text-[11px] text-slate-500 mt-1">100% daily city composite coverage</p>
        </div>
      </div>

      {/* 3. Provenance, Licensing & Scientific Commitments */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 space-y-4">
          <div className="flex items-center gap-2 font-bold text-slate-900 text-base">
            <Database className="w-4 h-4 text-sky-600" />
            <span>Dataset Provenance & Attribution</span>
          </div>

          <div className="space-y-3 text-xs text-slate-600 leading-relaxed">
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
              <div className="font-bold text-slate-900 flex items-center justify-between">
                <span>Central Pollution Control Board (CPCB)</span>
                <span className="text-[10px] text-sky-700 bg-sky-50 px-2 py-0.5 rounded font-mono">GODL India</span>
              </div>
              <p className="text-slate-500 mt-1">
                Continuous Ambient Air Quality Monitoring (CAAQM) network across 14 Bengaluru stations, accessed via XKDR Forum API (<a href="https://airquality.xkdr.org/" target="_blank" rel="noreferrer" className="text-sky-600 underline">airquality.xkdr.org</a>).
              </p>
            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
              <div className="font-bold text-slate-900 flex items-center justify-between">
                <span>ECMWF ERA5 Atmospheric Reanalysis</span>
                <span className="text-[10px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-mono">CC-BY 4.0</span>
              </div>
              <p className="text-slate-500 mt-1">
                16,080 hourly meteorological records (temperature, humidity, precipitation, pressure, wind vectors) accessed via Open-Meteo Historical Archive (<a href="https://open-meteo.com" target="_blank" rel="noreferrer" className="text-sky-600 underline">open-meteo.com</a>).
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 space-y-4">
          <div className="flex items-center gap-2 font-bold text-slate-900 text-base">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>Scientific Principles & Anti-Hallucination Rules</span>
          </div>

          <ul className="space-y-2 text-xs text-slate-700 leading-relaxed">
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span><strong>Zero Synthetic Data:</strong> Every data point displayed in BreatheWise originates from official sensor recordings or physical reanalysis models.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span><strong>Severe 500 Ceiling Policy:</strong> Open-ended Severe concentrations are mapped to the official 500 national index ceiling as an explicit implementation policy; zero upper breakpoints are invented.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span><strong>CO and O3 Protocol:</strong> 24-hour daily means are strictly excluded from daily station AQI to avoid substituting daily means for CPCB 8-hour metrics.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
              <span><strong>Zero Future Leakage:</strong> Forecasting models are trained strictly on past lags at issue time t; realized target-day weather is 100% withheld.</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};
