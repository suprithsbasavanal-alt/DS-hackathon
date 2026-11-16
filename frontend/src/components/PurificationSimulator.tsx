import React, { useState, useEffect, useId } from 'react';
import {
  Wind,
  ShieldCheck,
  AlertCircle,
  HelpCircle,
  Maximize2,
  Clock,
  Gauge,
  Sliders,
  Sparkles
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import { simulatePurification } from '../services/api';
import { PurificationSimulationResponse } from '../types';

interface PurificationSimulatorProps {
  initialOutdoorPm25?: number | null;
}

export const PurificationSimulator: React.FC<PurificationSimulatorProps> = ({
  initialOutdoorPm25 = 67.7
}) => {
  const [area, setArea] = useState<number>(20);
  const [height, setHeight] = useState<number>(2.8);
  const [initialPm25, setInitialPm25] = useState<number>(
    initialOutdoorPm25 ? Math.round(initialOutdoorPm25 * 10) / 10 : 67.7
  );
  const [cadr, setCadr] = useState<number>(300);
  const [runtime, setRuntime] = useState<number>(2.0);

  const [simulation, setSimulation] = useState<PurificationSimulationResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const areaId = useId();
  const heightId = useId();
  const pm25Id = useId();
  const cadrId = useId();
  const runtimeId = useId();

  // Run simulation on parameter changes
  useEffect(() => {
    let isMounted = true;
    const runSim = async () => {
      try {
        setLoading(true);
        setError(null);
        const res = await simulatePurification({
          room_area_m2: area,
          ceiling_height_m: height,
          initial_pm25_ug_m3: initialPm25,
          cadr_m3_h: cadr,
          runtime_hours: runtime
        });
        if (isMounted) setSimulation(res);
      } catch (err: any) {
        if (isMounted) setError(err?.message || 'Simulation calculation failed');
      } finally {
        if (isMounted) setLoading(false);
      }
    };

    const timeout = setTimeout(runSim, 100);
    return () => {
      isMounted = false;
      clearTimeout(timeout);
    };
  }, [area, height, initialPm25, cadr, runtime]);

  const volume = Math.round(area * height * 10) / 10;
  const ach = volume > 0 ? Math.round((cadr / volume) * 10) / 10 : 0;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-b border-slate-100 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-teal-50 text-teal-600 border border-teal-200">
              <Wind className="w-5 h-5" />
            </span>
            <div>
              <h3 className="font-bold text-slate-900 text-lg">
                Indoor Air Purification Simulator
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Physics-based first-order mass-balance exponential decay (Model PHYS-PURIFIER-01)
              </p>
            </div>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2 text-xs">
          <span className="px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 font-mono font-medium border border-slate-200">
            Formula: C(t) = C₀ · e^-(CADR/V)t
          </span>
          <span className="px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 font-medium border border-blue-200 flex items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5" />
            Deterministic Physics
          </span>
        </div>
      </div>

      {/* Mandatory Scientific Demarcation Banner */}
      <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 text-xs text-slate-600 space-y-1">
        <div className="flex items-center gap-1.5 font-semibold text-slate-800">
          <HelpCircle className="w-4 h-4 text-slate-500" />
          <span>Scientific Demarcation & Transparency:</span>
        </div>
        <p className="leading-relaxed">
          This calculator evaluates a <strong>theoretical first-order mass-balance decay scenario</strong> under user-specified geometric and mechanical assumptions. It is <strong>NOT an AI machine-learning prediction</strong>, nor does it represent an actual indoor sensor reading. No indoor particulate sensors were deployed in this project.
        </p>
      </div>

      {/* Main Grid: Controls vs Chart & Results */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Sliders Column (5 cols) */}
        <div className="lg:col-span-5 bg-slate-50/70 rounded-xl p-5 border border-slate-200 space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-600 flex items-center gap-1.5">
              <Sliders className="w-3.5 h-3.5" />
              Physical Parameters
            </span>
            <span className="text-xs font-mono text-slate-500">
              Vol: {volume} m³ · {ach} ACH
            </span>
          </div>

          {/* Area Slider */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs">
              <label htmlFor={areaId} className="font-semibold text-slate-700">
                Floor Area (m²)
              </label>
              <span className="font-mono font-bold text-slate-900 bg-white px-2 py-0.5 rounded border border-slate-200">
                {area} m² ({Math.round(area * 10.764)} sq ft)
              </span>
            </div>
            <input
              id={areaId}
              type="range"
              min={5}
              max={150}
              step={1}
              value={area}
              onChange={(e) => setArea(Number(e.target.value))}
              className="w-full accent-teal-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-400 font-mono">
              <span>5 m² (Studio)</span>
              <span>150 m² (Open Floor)</span>
            </div>
          </div>

          {/* Ceiling Height Slider */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs">
              <label htmlFor={heightId} className="font-semibold text-slate-700">
                Ceiling Height (m)
              </label>
              <span className="font-mono font-bold text-slate-900 bg-white px-2 py-0.5 rounded border border-slate-200">
                {height.toFixed(1)} m
              </span>
            </div>
            <input
              id={heightId}
              type="range"
              min={2.0}
              max={4.5}
              step={0.1}
              value={height}
              onChange={(e) => setHeight(Number(e.target.value))}
              className="w-full accent-teal-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-400 font-mono">
              <span>2.0 m</span>
              <span>4.5 m (High ceiling)</span>
            </div>
          </div>

          {/* Initial PM2.5 */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs">
              <label htmlFor={pm25Id} className="font-semibold text-slate-700">
                Starting PM2.5 (C₀)
              </label>
              <span className="font-mono font-bold text-slate-900 bg-white px-2 py-0.5 rounded border border-slate-200">
                {initialPm25} µg/m³
              </span>
            </div>
            <input
              id={pm25Id}
              type="range"
              min={5}
              max={300}
              step={1}
              value={initialPm25}
              onChange={(e) => setInitialPm25(Number(e.target.value))}
              className="w-full accent-teal-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-400 font-mono">
              <span>5 µg/m³ (Clean)</span>
              <span>300 µg/m³ (Severe)</span>
            </div>
          </div>

          {/* Purifier CADR */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs">
              <label htmlFor={cadrId} className="font-semibold text-slate-700">
                Purifier CADR (m³/h)
              </label>
              <span className="font-mono font-bold text-slate-900 bg-white px-2 py-0.5 rounded border border-slate-200">
                {cadr} m³/h
              </span>
            </div>
            <input
              id={cadrId}
              type="range"
              min={0}
              max={800}
              step={10}
              value={cadr}
              onChange={(e) => setCadr(Number(e.target.value))}
              className="w-full accent-teal-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-400 font-mono">
              <span>0 (Off)</span>
              <span>800 m³/h (Commercial)</span>
            </div>
          </div>

          {/* Runtime Slider */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs">
              <label htmlFor={runtimeId} className="font-semibold text-slate-700">
                Operating Runtime (hours)
              </label>
              <span className="font-mono font-bold text-slate-900 bg-white px-2 py-0.5 rounded border border-slate-200">
                {runtime.toFixed(1)} h ({Math.round(runtime * 60)} min)
              </span>
            </div>
            <input
              id={runtimeId}
              type="range"
              min={0}
              max={6.0}
              step={0.1}
              value={runtime}
              onChange={(e) => setRuntime(Number(e.target.value))}
              className="w-full accent-teal-600 h-2 bg-slate-200 rounded-lg cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-400 font-mono">
              <span>0 h</span>
              <span>6.0 h</span>
            </div>
          </div>
        </div>

        {/* Results & Visual Graph Column (7 cols) */}
        <div className="lg:col-span-7 flex flex-col justify-between space-y-4">
          {/* Key Metric KPI Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 text-center">
              <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">
                Room Volume
              </span>
              <span className="text-lg font-bold font-mono text-slate-900">
                {simulation?.room_volume_m3 ?? volume}
              </span>
              <span className="text-[10px] text-slate-500 block">m³ space</span>
            </div>

            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 text-center">
              <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block">
                CADR Rate
              </span>
              <span className="text-lg font-bold font-mono text-teal-700">
                {simulation?.air_changes_per_hour_cadr ?? ach}
              </span>
              <span className="text-[10px] text-slate-500 block">air changes / hr</span>
            </div>

            <div className="bg-teal-50/70 border border-teal-200 rounded-xl p-3 text-center">
              <span className="text-[11px] font-semibold text-teal-800 uppercase tracking-wider block">
                Final PM2.5
              </span>
              <span className="text-lg font-bold font-mono text-teal-900">
                {simulation?.final_pm25_ug_m3 ?? initialPm25}
              </span>
              <span className="text-[10px] text-teal-700 block">µg/m³ remaining</span>
            </div>

            <div className="bg-emerald-50/70 border border-emerald-200 rounded-xl p-3 text-center">
              <span className="text-[11px] font-semibold text-emerald-800 uppercase tracking-wider block">
                Reduction
              </span>
              <span className="text-lg font-bold font-mono text-emerald-900">
                {simulation?.percentage_reduction ?? 0}%
              </span>
              <span className="text-[10px] text-emerald-700 block">theoretical cleanup</span>
            </div>
          </div>

          {/* Decay Graph */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
            <div className="flex items-center justify-between mb-3 text-xs">
              <span className="font-bold text-slate-800 flex items-center gap-1.5">
                <Gauge className="w-3.5 h-3.5 text-teal-600" />
                PM2.5 Mass Concentration Decay Curve
              </span>
              <div className="flex items-center gap-3 font-mono text-[11px] text-slate-500">
                <span className="flex items-center gap-1">
                  <span className="w-2.5 h-0.5 bg-teal-600 inline-block"></span> C(t)
                </span>
                <span className="flex items-center gap-1">
                  <span className="w-2.5 h-0.5 bg-amber-500 border-b border-dashed inline-block"></span> CPCB 24h (60)
                </span>
              </div>
            </div>

            <div className="h-56 w-full">
              {simulation && simulation.decay_curve.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={simulation.decay_curve}
                    margin={{ top: 10, right: 15, left: -20, bottom: 0 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                    <XAxis
                      dataKey="time_hours"
                      tick={{ fontSize: 11, fill: '#64748b' }}
                      tickFormatter={(val) => `${Number(val).toFixed(1)}h`}
                    />
                    <YAxis
                      domain={[0, 'auto']}
                      tick={{ fontSize: 11, fill: '#64748b' }}
                    />
                    <Tooltip
                      content={({ active, payload }) => {
                        if (active && payload && payload.length) {
                          const data = payload[0].payload;
                          return (
                            <div className="bg-slate-900 text-white rounded-lg p-2.5 text-xs shadow-lg space-y-1">
                              <p className="font-semibold text-slate-300">
                                Time: {data.time_hours} hours ({Math.round(data.time_hours * 60)} min)
                              </p>
                              <p className="font-mono text-teal-300 font-bold">
                                PM2.5: {data.pm25_ug_m3} µg/m³
                              </p>
                              <p className="text-[11px] text-slate-400">
                                Reduction: {data.reduction_pct}%
                              </p>
                            </div>
                          );
                        }
                        return null;
                      }}
                    />
                    <ReferenceLine
                      y={60}
                      stroke="#f59e0b"
                      strokeDasharray="4 4"
                      label={{
                        value: 'CPCB 60',
                        position: 'insideTopRight',
                        fill: '#d97706',
                        fontSize: 10
                      }}
                    />
                    <Line
                      type="monotone"
                      dataKey="pm25_ug_m3"
                      stroke="#0d9488"
                      strokeWidth={2.5}
                      dot={false}
                      activeDot={{ r: 5, fill: '#0d9488' }}
                      isAnimationActive={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-xs text-slate-400 font-mono">
                  Loading decay calculation...
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Assumptions Ledger */}
      <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-2">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
          <AlertCircle className="w-3.5 h-3.5 text-slate-500" />
          5 Essential Physical Idealizing Assumptions (Model PHYS-PURIFIER-01)
        </h4>
        <ol className="list-decimal list-inside text-xs text-slate-600 space-y-1 leading-relaxed">
          {simulation?.assumptions_ledger ? (
            simulation.assumptions_ledger.map((item, idx) => (
              <li key={idx} className="pl-1">
                <span>{item}</span>
              </li>
            ))
          ) : (
            <>
              <li>Instantaneous and perfect spatial mixing throughout the room volume.</li>
              <li>Zero continuing indoor emission sources.</li>
              <li>Zero building envelope infiltration/exfiltration (ACH_nat = 0).</li>
              <li>Zero natural particle deposition or wall adsorption.</li>
              <li>Continuous operation at rated CADR with clean filter.</li>
            </>
          )}
        </ol>
      </div>
    </div>
  );
};
