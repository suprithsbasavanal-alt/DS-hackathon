import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Wind,
  ShieldAlert,
  Layers,
  Thermometer,
  Compass,
  Activity,
  CheckCircle2,
  AlertTriangle,
  Info,
  Calendar,
  RefreshCw,
  Search,
  Filter,
  BarChart2,
  ArrowRight
} from 'lucide-react';
import {
  fetchAIInsights,
  fetchRegimes,
  fetchHealthAdvisories
} from '../services/api';
import {
  EnvironmentalInsightsResponse,
  EnvironmentalRegimesResponse,
  HealthAdvisoryResponse,
  StationMeta
} from '../types';
import { PurificationSimulator } from '../components/PurificationSimulator';

interface AIInsightsViewProps {
  stations?: StationMeta[];
}

export const AIInsightsView: React.FC<AIInsightsViewProps> = ({ stations = [] }) => {
  const [selectedStation, setSelectedStation] = useState<string>('city_composite');
  const [selectedDate, setSelectedDate] = useState<string>('2024-10-31');
  const [forceFallback, setForceFallback] = useState<boolean>(false);

  // Hypothetical AQI test state
  const [hypotheticalAqi, setHypotheticalAqi] = useState<number | ''>('');

  // Data states
  const [insights, setInsights] = useState<EnvironmentalInsightsResponse | null>(null);
  const [regimes, setRegimes] = useState<EnvironmentalRegimesResponse | null>(null);
  const [healthAdvisory, setHealthAdvisory] = useState<HealthAdvisoryResponse | null>(null);

  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [insightsRes, regimesRes, healthRes] = await Promise.all([
        fetchAIInsights(selectedStation, selectedDate),
        fetchRegimes(forceFallback),
        fetchHealthAdvisories(
          hypotheticalAqi !== '' ? Number(hypotheticalAqi) : undefined,
          selectedStation,
          selectedDate
        )
      ]);

      setInsights(insightsRes);
      setRegimes(regimesRes);
      setHealthAdvisory(healthRes);
    } catch (err: any) {
      console.error('Error fetching AI insights:', err);
      setError(err?.message || 'Failed to load environmental intelligence.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedStation, selectedDate, forceFallback, hypotheticalAqi]);

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Top Banner & Station / Date Selector */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="p-2 rounded-xl bg-sky-50 text-sky-600 border border-sky-200">
                <Sparkles className="w-5 h-5" />
              </span>
              <div>
                <h1 className="text-xl font-bold text-slate-900 tracking-tight">
                  Environmental Intelligence & AI Decision Arena
                </h1>
                <p className="text-xs text-slate-500 font-medium">
                  CPCB Table 3.2 threshold adapter, orthogonal wind decomposition, unsupervised environmental regimes, and physics simulation
                </p>
              </div>
            </div>
          </div>

          {/* Controls: Station & Date Picker */}
          <div className="flex flex-wrap items-center gap-3">
            <div>
              <label htmlFor="ai-station-select" className="block text-[10px] font-semibold uppercase tracking-wider text-slate-400 mb-1">
                Monitoring Scope
              </label>
              <select
                id="ai-station-select"
                aria-label="Monitoring Scope"
                value={selectedStation}
                onChange={(e) => setSelectedStation(e.target.value)}
                className="bg-slate-50 border border-slate-200 text-xs rounded-xl px-3 py-1.5 font-medium text-slate-800 focus:outline-none focus:ring-2 focus:ring-sky-500"
              >
                <option value="city_composite">City Composite (All Active CAAQMS)</option>
                {stations.map((st) => (
                  <option key={st.station_id} value={st.station_id}>
                    {st.station_name} {st.is_active ? '' : '(Decommissioned)'}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="ai-date-select" className="block text-[10px] font-semibold uppercase tracking-wider text-slate-400 mb-1">
                Archive Date
              </label>
              <select
                id="ai-date-select"
                aria-label="Archive Date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="bg-slate-50 border border-slate-200 text-xs rounded-xl px-3 py-1.5 font-medium text-slate-800 font-mono focus:outline-none focus:ring-2 focus:ring-sky-500"
              >
                <option value="2024-10-31">2024-10-31 (Latest Verified)</option>
                <option value="2024-05-15">2024-05-15 (Summer Pattern)</option>
                <option value="2024-07-20">2024-07-20 (Monsoon Pattern)</option>
                <option value="2024-01-10">2024-01-10 (Winter Inversion)</option>
                <option value="2023-11-12">2023-11-12 (Diwali Observation)</option>
              </select>
            </div>

            <div className="self-end">
              <button
                onClick={loadData}
                disabled={loading}
                className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition"
                title="Refresh AI Insights"
              >
                <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-sky-600' : ''}`} />
              </button>
            </div>
          </div>
        </div>

        {/* Observation Status Pill Bar */}
        {insights && (
          <div className="flex flex-wrap items-center gap-3 pt-3 border-t border-slate-100 text-xs">
            <span className="font-semibold text-slate-700">
              Station: <span className="font-mono text-slate-900">{insights.station?.name ?? selectedStation}</span>
            </span>
            <span className="text-slate-300">|</span>
            <span>
              Target AQI:{' '}
              <span className="font-bold font-mono text-sky-700">
                {insights.aqi_summary?.aqi ?? 'N/A'}
              </span>{' '}
              ({insights.aqi_summary?.category})
            </span>
            <span className="text-slate-300">|</span>
            <span>
              Prominent Pollutant:{' '}
              <span className="font-semibold text-slate-800">
                {insights.aqi_summary?.prominent_pollutant ?? 'None'}
              </span>
            </span>
            {insights.station?.active_stations_count !== undefined && (
              <>
                <span className="text-slate-300">|</span>
                <span className="text-slate-500 font-mono text-[11px]">
                  Contributing Stations: {insights.station.active_stations_count}
                </span>
              </>
            )}
          </div>
        )}
      </div>

      {/* SECTION 1: Criteria Pollutants Threshold Table & Meteorological Vector */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Criteria Pollutants Table (7 cols) */}
        <div className="lg:col-span-8 bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-sky-600" />
              <h3 className="font-bold text-slate-900 text-base">
                Criteria Pollutants Assessment (CPCB Table 3.2 Standards)
              </h3>
            </div>
            <span className="text-[11px] font-mono text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
              24-Hour Regulatory Window
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-semibold uppercase text-[10px] tracking-wider border-b border-slate-200">
                <tr>
                  <th className="py-2.5 px-3">Pollutant</th>
                  <th className="py-2.5 px-3">Concentration</th>
                  <th className="py-2.5 px-3">Averaging Window</th>
                  <th className="py-2.5 px-3">Sub-Index</th>
                  <th className="py-2.5 px-3">Category Tier</th>
                  <th className="py-2.5 px-3">Regulatory Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {insights?.pollutants.map((p) => {
                  const isLead = p.name === 'Pb' || p.tier.includes('Not available');
                  const is8h = p.tier.includes('8h standard only');
                  const isProminent = insights.aqi_summary?.prominent_pollutant === p.name;

                  return (
                    <tr
                      key={p.name}
                      className={isProminent ? 'bg-amber-50/50 font-medium' : 'hover:bg-slate-50/50'}
                    >
                      <td className="py-2.5 px-3 font-semibold text-slate-800 flex items-center gap-1.5">
                        <span>{p.display_name || p.name}</span>
                        {isProminent && (
                          <span className="text-[9px] bg-amber-100 text-amber-800 font-bold px-1.5 py-0.2 rounded border border-amber-200">
                            PROMINENT
                          </span>
                        )}
                      </td>
                      <td className="py-2.5 px-3 font-mono text-slate-900">
                        {p.concentration !== null ? `${p.concentration} ${p.unit}` : (
                          <span className="text-slate-400 italic">Not available</span>
                        )}
                      </td>
                      <td className="py-2.5 px-3 font-mono text-slate-600">
                        {p.averaging_period}
                      </td>
                      <td className="py-2.5 px-3 font-mono">
                        {p.sub_index !== null ? (
                          <span className="font-bold text-slate-800">{p.sub_index}</span>
                        ) : (
                          <span className="text-slate-400 italic">null</span>
                        )}
                      </td>
                      <td className="py-2.5 px-3 text-slate-700">
                        <span className="text-[11px] font-medium">{p.tier}</span>
                      </td>
                      <td className="py-2.5 px-3">
                        {isLead ? (
                          <span className="px-2 py-0.5 rounded text-[10px] bg-slate-100 text-slate-600 font-medium border border-slate-200">
                            Unmonitored
                          </span>
                        ) : is8h ? (
                          <span className="px-2 py-0.5 rounded text-[10px] bg-purple-50 text-purple-700 font-medium border border-purple-200">
                            8h Std Only
                          </span>
                        ) : p.sub_index !== null && p.sub_index > 100 ? (
                          <span className="px-2 py-0.5 rounded text-[10px] bg-red-100 text-red-800 font-bold border border-red-200">
                            Elevated
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-100 text-emerald-800 font-medium border border-emerald-200">
                            Within Limits
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          <div className="bg-slate-50 rounded-xl p-3 text-[11px] text-slate-500 space-y-1 border border-slate-200">
            <p>
              <strong>CPCB Compliance Safeguards:</strong> Under Central Pollution Control Board (CPCB) Table 3.2 rules, Carbon Monoxide (CO) and Ozone (O₃) sub-indices are defined strictly for 8-hour exposure averages. Daily 24-hour averages yield <code className="bg-white px-1 py-0.2 rounded border">sub_index: null</code> to prevent non-compliant statutory sub-index generation. Lead (Pb) was not monitored in this deployment and is transparently recorded as unavailable.
            </p>
          </div>
        </div>

        {/* Meteorology & Wind Vector Decomposition (4 cols) */}
        <div className="lg:col-span-4 bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
            <Thermometer className="w-5 h-5 text-amber-500" />
            <h3 className="font-bold text-slate-900 text-base">
              Meteorological Context & Wind Decomposition
            </h3>
          </div>

          {insights?.meteorology && (
            <div className="space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-2.5">
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <span className="text-[10px] uppercase font-bold text-slate-500 block">Temperature</span>
                  <span className="text-base font-bold font-mono text-slate-900">
                    {insights.meteorology.temperature_mean ?? '—'} °C
                  </span>
                </div>
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <span className="text-[10px] uppercase font-bold text-slate-500 block">Humidity</span>
                  <span className="text-base font-bold font-mono text-slate-900">
                    {insights.meteorology.humidity_mean ?? '—'}%
                  </span>
                </div>
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <span className="text-[10px] uppercase font-bold text-slate-500 block">Surface Pressure</span>
                  <span className="text-base font-bold font-mono text-slate-900">
                    {insights.meteorology.pressure_mean ?? '—'} hPa
                  </span>
                </div>
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <span className="text-[10px] uppercase font-bold text-slate-500 block">Precipitation</span>
                  <span className="text-base font-bold font-mono text-slate-900">
                    {insights.meteorology.precipitation_sum ?? '—'} mm
                  </span>
                </div>
              </div>

              {/* Orthogonal Wind Components */}
              <div className="bg-sky-50/70 border border-sky-200 rounded-xl p-3.5 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-sky-950 flex items-center gap-1.5">
                    <Compass className="w-4 h-4 text-sky-600" />
                    Orthogonal Wind Vectors (u, v)
                  </span>
                  <span className="text-[10px] font-mono text-sky-800 bg-white px-2 py-0.5 rounded border border-sky-200">
                    d=8 Orthogonal
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-2 pt-1 font-mono text-xs">
                  <div className="bg-white p-2 rounded-lg border border-sky-100">
                    <span className="text-[10px] text-slate-500 block">Zonal (u) [E-W]</span>
                    <span className="font-bold text-slate-900">
                      {insights.meteorology.wind_u ?? '—'} km/h
                    </span>
                  </div>
                  <div className="bg-white p-2 rounded-lg border border-sky-100">
                    <span className="text-[10px] text-slate-500 block">Meridional (v) [N-S]</span>
                    <span className="font-bold text-slate-900">
                      {insights.meteorology.wind_v ?? '—'} km/h
                    </span>
                  </div>
                </div>

                <p className="text-[10px] text-sky-900 leading-relaxed">
                  Resultant Speed: <span className="font-mono font-semibold">{insights.meteorology.wind_speed_resultant} km/h</span> at <span className="font-mono font-semibold">{insights.meteorology.wind_dir_resultant}°</span>. Scalar wind speed is excluded from clustering features to prevent collinear double-counting ({'WS = √(u² + v²)'}).
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* SECTION 2: Retrospective Correlation Matrix */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <BarChart2 className="w-5 h-5 text-indigo-600" />
            <h3 className="font-bold text-slate-900 text-base">
              Retrospective Meteorological Correlation Matrix (N = 670 Historical Days)
            </h3>
          </div>
          {insights?.correlation_scope && (
            <span className="text-xs px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-800 font-mono font-medium border border-indigo-200">
              Scope: {insights.correlation_scope}
            </span>
          )}
        </div>

        {insights?.correlations && insights.correlations.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {insights.correlations.slice(0, 6).map((c, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:shadow-sm transition space-y-2 text-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-900 font-mono">
                    {c.metric_x} ↔ {c.metric_y}
                  </span>
                  <span
                    className={`font-mono font-bold px-2 py-0.5 rounded text-[11px] ${
                      c.pearson_r > 0
                        ? 'bg-amber-100 text-amber-900 border border-amber-200'
                        : 'bg-teal-100 text-teal-900 border border-teal-200'
                    }`}
                  >
                    r = {c.pearson_r > 0 ? `+${c.pearson_r}` : c.pearson_r}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-[10px] text-slate-500 font-mono">
                  <span>N = {c.n_samples} days</span>
                  {c.spearman_rho !== undefined && (
                    <>
                      <span>•</span>
                      <span>ρ = {c.spearman_rho}</span>
                    </>
                  )}
                </div>
                <p className="text-[11px] text-slate-600 leading-relaxed">
                  {c.description}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-6 text-center text-xs text-slate-500 bg-slate-50 rounded-xl border border-slate-200">
            No station-level correlations displayed for this selection. (Citywide correlations are strictly omitted for decommissioned stations to prevent regional conflation).
          </div>
        )}
      </div>

      {/* SECTION 3: Exploratory Environmental Regimes & Deterministic Fallback */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2">
              <Layers className="w-5 h-5 text-teal-600" />
              <h3 className="font-bold text-slate-900 text-base">
                Exploratory Environmental Regimes (Unsupervised k-Means, d=8)
              </h3>
            </div>
            <p className="text-xs text-slate-500">
              Optimal k=3 clustering across 670 daily observations using non-redundant orthogonal meteorological and pollutant features
            </p>
          </div>

          {/* Toggle for Deterministic Fallback */}
          <div className="flex items-center gap-3">
            <label className="flex items-center gap-2 text-xs font-semibold text-slate-700 cursor-pointer">
              <input
                type="checkbox"
                checked={forceFallback}
                onChange={(e) => setForceFallback(e.target.checked)}
                className="rounded text-teal-600 focus:ring-teal-500 w-4 h-4"
              />
              <span>Force Deterministic Seasonal Fallback</span>
            </label>
          </div>
        </div>

        {/* Diagnostic Metrics Strip */}
        {regimes && (
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 text-xs">
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-center">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block">Methodology</span>
              <span className="font-bold text-slate-900 text-sm">
                {regimes.is_fallback ? 'Seasonal Fallback' : 'k-Means (k=3)'}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-center">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block">Silhouette Score</span>
              <span className="font-bold font-mono text-teal-700 text-sm">
                {regimes.diagnostic_metrics.silhouette_score}
              </span>
              <span className="text-[10px] text-slate-400 block">Heuristic &ge; 0.30</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-center">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block">Feature Dim (d)</span>
              <span className="font-bold font-mono text-slate-900 text-sm">
                d = {regimes.diagnostic_metrics.feature_dim}
              </span>
              <span className="text-[10px] text-slate-400 block">Orthogonal features</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-center">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block">Multi-Seed ARI</span>
              <span className="font-bold font-mono text-emerald-700 text-sm">
                ARI = {regimes.diagnostic_metrics.multi_seed_stability_ari.toFixed(4)}
              </span>
              <span className="text-[10px] text-slate-400 block">5 Seeds (100% Invariant)</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-center">
              <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block">Observations</span>
              <span className="font-bold font-mono text-slate-900 text-sm">
                N = 670
              </span>
              <span className="text-[10px] text-slate-400 block">100% Accounted</span>
            </div>
          </div>
        )}

        {/* 3 Regime Profile Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {regimes?.regimes.map((rg) => (
            <div
              key={rg.cluster_id}
              className="p-5 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:shadow-md transition space-y-3"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-teal-800 bg-teal-50 px-2 py-0.5 rounded border border-teal-200">
                  Cluster {rg.cluster_id}
                </span>
                <span className="text-xs font-mono font-semibold text-slate-600">
                  {rg.sample_count} days ({rg.sample_percentage}%)
                </span>
              </div>

              <div>
                <h4 className="font-bold text-slate-900 text-sm">{rg.name}</h4>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  {rg.description}
                </p>
              </div>

              {/* Mean Parameters Table */}
              <div className="pt-2 border-t border-slate-200 grid grid-cols-2 gap-2 text-xs font-mono">
                <div>
                  <span className="text-[10px] text-slate-500 font-sans block">Mean AQI</span>
                  <span className="font-bold text-slate-900">{rg.mean_aqi} ({rg.mean_category})</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-500 font-sans block">Dominant Months</span>
                  <span className="font-semibold text-slate-800 font-sans text-[11px]">{rg.dominant_months}</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-500 font-sans block">Centroid PM2.5</span>
                  <span className="font-medium text-slate-800">{rg.centroid.pm25} µg/m³</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-500 font-sans block">Centroid PM10</span>
                  <span className="font-medium text-slate-800">{rg.centroid.pm10} µg/m³</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-500 font-sans block">Centroid Temp</span>
                  <span className="font-medium text-slate-800">{rg.centroid.temp_mean} °C</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-500 font-sans block">Centroid Humidity</span>
                  <span className="font-medium text-slate-800">{rg.centroid.humidity_mean}%</span>
                </div>
              </div>

              {/* Empirical Quantiles Display if available */}
              {rg.quantiles?.city_aqi && (
                <div className="pt-2 border-t border-slate-200 text-[10px] font-mono text-slate-500">
                  <span className="font-sans font-semibold text-slate-700 block mb-0.5">AQI Quantiles:</span>
                  <span>p0:{rg.quantiles.city_aqi.p0} | p25:{rg.quantiles.city_aqi.p25} | p50:{rg.quantiles.city_aqi.p50} | p75:{rg.quantiles.city_aqi.p75} | p100:{rg.quantiles.city_aqi.p100}</span>
                </div>
              )}
            </div>
          ))}
        </div>

        <p className="text-[11px] text-slate-500 italic">
          <strong>Scientific Disclaimer:</strong> {regimes?.disclaimer}
        </p>
      </div>

      {/* SECTION 4: Deterministic CPCB Health Advisories & Sensitive Group Guidance */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-amber-600" />
              <h3 className="font-bold text-slate-900 text-base">
                Deterministic CPCB Health Advisory Engine
              </h3>
            </div>
            <p className="text-xs text-slate-500">
              Rule-based mapping from CPCB Table 3.2 regulatory bands with trigger evidence and sensitive cohort actions
            </p>
          </div>

          {/* Interactive Hypothetical AQI tester */}
          <div className="flex items-center gap-2">
            <label htmlFor="ai-hypothetical-aqi" className="text-xs font-semibold text-slate-700 whitespace-nowrap">
              Test Custom AQI:
            </label>
            <input
              id="ai-hypothetical-aqi"
              aria-label="Test Custom AQI"
              type="number"
              min={0}
              max={500}
              placeholder="e.g. 245"
              value={hypotheticalAqi}
              onChange={(e) => {
                const val = e.target.value;
                setHypotheticalAqi(val === '' ? '' : Number(val));
              }}
              className="w-24 bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1 text-xs font-mono focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
            {hypotheticalAqi !== '' && (
              <button
                onClick={() => setHypotheticalAqi('')}
                className="text-[11px] text-slate-500 hover:text-slate-800 underline"
              >
                Reset
              </button>
            )}
          </div>
        </div>

        {/* Advisory Cards */}
        <div className="space-y-4">
          {healthAdvisory?.advisories.map((adv) => (
            <div
              key={adv.rule_id}
              className="p-5 rounded-2xl border border-slate-200 bg-slate-50/70 space-y-3"
            >
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold px-2.5 py-1 rounded-md bg-amber-100 text-amber-900 border border-amber-200">
                    {adv.rule_id}
                  </span>
                  <span className="font-bold text-sm text-slate-900">{adv.category}</span>
                </div>
                <span className="text-xs font-mono font-semibold text-slate-600 bg-white px-2.5 py-1 rounded border border-slate-200">
                  Trigger: {adv.trigger_metric}
                </span>
              </div>

              {/* Public & Sensitive Advice */}
              <div className="space-y-2 text-xs">
                <div>
                  <span className="font-bold text-slate-800 block mb-0.5">General Public Guidance:</span>
                  <p className="text-slate-700 leading-relaxed">{adv.general_public_advice}</p>
                </div>

                <div className="pt-2 border-t border-slate-200">
                  <span className="font-bold text-slate-800 block mb-1">Specific Cohort Actions:</span>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <div className="bg-white p-3 rounded-xl border border-slate-200 space-y-1">
                      <span className="font-semibold text-teal-800 text-[11px] block">
                        Asthma & Respiratory
                      </span>
                      <p className="text-slate-600 text-[11px] leading-relaxed">
                        {adv.sensitive_groups_advice.asthma}
                      </p>
                    </div>

                    <div className="bg-white p-3 rounded-xl border border-slate-200 space-y-1">
                      <span className="font-semibold text-amber-800 text-[11px] block">
                        Children & Elderly
                      </span>
                      <p className="text-slate-600 text-[11px] leading-relaxed">
                        {adv.sensitive_groups_advice.elderly_and_children}
                      </p>
                    </div>

                    <div className="bg-white p-3 rounded-xl border border-slate-200 space-y-1">
                      <span className="font-semibold text-sky-800 text-[11px] block">
                        Outdoor Workers
                      </span>
                      <p className="text-slate-600 text-[11px] leading-relaxed">
                        {adv.sensitive_groups_advice.outdoor_workers}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="pt-2">
                  <span className="font-bold text-slate-800 inline-block mr-1">Outdoor Physical Activity:</span>
                  <span className="text-slate-700">{adv.outdoor_activity_recommendation}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="bg-slate-100/70 border border-slate-200 rounded-xl p-3 text-xs text-slate-500">
          <strong>Medical Notice:</strong> {healthAdvisory?.medical_disclaimer}
        </div>
      </div>

      {/* SECTION 5: Indoor Air Purification Physics Simulator */}
      <PurificationSimulator
        initialOutdoorPm25={
          insights?.pollutants.find((p) => p.name === 'PM2.5')?.concentration ?? 67.7
        }
      />
    </div>
  );
};
