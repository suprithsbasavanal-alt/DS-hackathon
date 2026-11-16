import React, { useState } from 'react';
import {
  TrendRecord,
  WeatherImpact,
  DiurnalData
} from '../types';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar
} from 'recharts';
import {
  SlidersHorizontal,
  Calendar,
  Wind,
  Info,
  Clock,
  HelpCircle
} from 'lucide-react';

interface ExplorerViewProps {
  trends: TrendRecord[];
  weatherImpact: WeatherImpact | null;
  diurnalData: DiurnalData | null;
  loading: boolean;
}

export const ExplorerView: React.FC<ExplorerViewProps> = ({
  trends,
  weatherImpact,
  diurnalData,
  loading
}) => {
  const [timeRange, setTimeRange] = useState<'1M' | '3M' | '6M' | '1Y' | 'ALL'>('3M');
  const [selectedPollutants, setSelectedPollutants] = useState<{ [key: string]: boolean }>({
    city_aqi: true,
    pm25: true,
    pm10: false,
    no2: false,
    so2: false,
    co: false,
    o3: false
  });
  const [selectedDiurnalStation, setSelectedDiurnalStation] = useState<'BTM Layout' | 'Peenya'>('BTM Layout');

  if (loading || !trends.length) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <div className="w-10 h-10 border-4 border-sky-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm font-medium text-slate-500">Loading Multi-Pollutant Time Series...</p>
      </div>
    );
  }

  // Filter trends by range
  const filterTrendsByRange = () => {
    if (timeRange === 'ALL') return trends;
    const daysMap = { '1M': 30, '3M': 90, '6M': 180, '1Y': 365 };
    const cutoffDays = daysMap[timeRange];
    return trends.slice(-cutoffDays);
  };

  const filteredTrends = filterTrendsByRange();

  const togglePollutant = (key: string) => {
    setSelectedPollutants((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  // Diurnal curve data for selected landmark station
  const stationDiurnal = diurnalData?.[selectedDiurnalStation]?.diurnal_curves || {};
  const diurnalHours = Array.from({ length: 24 }, (_, i) => i);
  const diurnalChartData = diurnalHours.map((h) => ({
    hour: `${h.toString().padStart(2, '0')}:00`,
    hourNum: h,
    PM25: stationDiurnal['PM2.5']?.[h]?.mean_concentration ?? null,
    PM10: stationDiurnal['PM10']?.[h]?.mean_concentration ?? null,
    NO2: stationDiurnal['NO2']?.[h]?.mean_concentration ?? null,
    CO: stationDiurnal['CO']?.[h]?.mean_concentration ? stationDiurnal['CO'][h].mean_concentration * 10 : null, // scaled for display
  }));

  return (
    <div className="space-y-8">
      {/* View Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Historical Air Quality & Meteorological Explorer
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Explore continuous multi-pollutant daily trends (2023–2024), 24-hour diurnal commute patterns, and retrospective weather associations.
        </p>
      </div>

      {/* 1. Multi-Pollutant Historical Trends */}
      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-100">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Historical Time Series (670 Calendar Days)</h2>
            <p className="text-xs text-slate-400 mt-0.5">Continuous composite daily records from Jan 1, 2023 to Oct 31, 2024</p>
          </div>

          {/* Time range buttons */}
          <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl text-xs font-semibold">
            {(['1M', '3M', '6M', '1Y', 'ALL'] as const).map((range) => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  timeRange === range
                    ? 'bg-white text-slate-900 shadow-sm font-bold'
                    : 'text-slate-500 hover:text-slate-900'
                }`}
              >
                {range}
              </button>
            ))}
          </div>
        </div>

        {/* Pollutant selector pills */}
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider mr-2">Parameters:</span>
          {[
            { id: 'city_aqi', label: 'City AQI', color: '#0ea5e9' },
            { id: 'pm25', label: 'PM2.5 (µg/m³)', color: '#8b5cf6' },
            { id: 'pm10', label: 'PM10 (µg/m³)', color: '#f59e0b' },
            { id: 'no2', label: 'NO2 (µg/m³)', color: '#ec4899' },
            { id: 'so2', label: 'SO2 (µg/m³)', color: '#10b981' },
            { id: 'co', label: 'CO (mg/m³)', color: '#f97316' },
            { id: 'o3', label: 'Ozone (µg/m³)', color: '#06b6d4' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => togglePollutant(item.id)}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border transition-all ${
                selectedPollutants[item.id]
                  ? 'bg-slate-900 text-white border-slate-900 shadow-sm'
                  : 'bg-white text-slate-600 border-slate-200 hover:border-slate-300'
              }`}
            >
              <span className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color }}></span>
              <span>{item.label}</span>
            </button>
          ))}
        </div>

        {/* Recharts Main Trends LineChart */}
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={filteredTrends} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#94a3b8' }} tickFormatter={(d) => d.slice(5)} />
              <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} domain={[0, 'auto']} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderRadius: '8px', border: 'none', color: '#fff', fontSize: '12px' }}
                labelStyle={{ color: '#94a3b8', fontSize: '11px', marginBottom: '4px' }}
              />
              <Legend verticalAlign="top" height={36} wrapperStyle={{ fontSize: '12px', paddingBottom: '12px' }} />
              {selectedPollutants.city_aqi && (
                <Line type="monotone" dataKey="city_aqi" name="City Composite AQI" stroke="#0ea5e9" strokeWidth={2.5} dot={false} />
              )}
              {selectedPollutants.pm25 && (
                <Line type="monotone" dataKey="pm25" name="PM2.5 (µg/m³)" stroke="#8b5cf6" strokeWidth={1.8} dot={false} />
              )}
              {selectedPollutants.pm10 && (
                <Line type="monotone" dataKey="pm10" name="PM10 (µg/m³)" stroke="#f59e0b" strokeWidth={1.8} dot={false} />
              )}
              {selectedPollutants.no2 && (
                <Line type="monotone" dataKey="no2" name="NO2 (µg/m³)" stroke="#ec4899" strokeWidth={1.5} dot={false} />
              )}
              {selectedPollutants.so2 && (
                <Line type="monotone" dataKey="so2" name="SO2 (µg/m³)" stroke="#10b981" strokeWidth={1.5} dot={false} />
              )}
              {selectedPollutants.co && (
                <Line type="monotone" dataKey="co" name="CO (mg/m³)" stroke="#f97316" strokeWidth={1.5} dot={false} />
              )}
              {selectedPollutants.o3 && (
                <Line type="monotone" dataKey="o3" name="Ozone (µg/m³)" stroke="#06b6d4" strokeWidth={1.5} dot={false} />
              )}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 2. Diurnal Hourly Commuter Profiles & Weather Associations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Diurnal Curves Card */}
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-1.5">
                <Clock className="w-4 h-4 text-sky-600" />
                <h3 className="font-bold text-slate-900 text-base">Diurnal Commute Profiles (24 Hours)</h3>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">Empirical hourly averages across benchmark seasonal months (2024)</p>
            </div>

            <div className="flex items-center bg-slate-100 p-0.5 rounded-lg text-xs font-semibold">
              <button
                onClick={() => setSelectedDiurnalStation('BTM Layout')}
                className={`px-2.5 py-1 rounded-md transition ${selectedDiurnalStation === 'BTM Layout' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500'}`}
              >
                BTM Layout
              </button>
              <button
                onClick={() => setSelectedDiurnalStation('Peenya')}
                className={`px-2.5 py-1 rounded-md transition ${selectedDiurnalStation === 'Peenya' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500'}`}
              >
                Peenya
              </button>
            </div>
          </div>

          {/* Diurnal Curve Chart */}
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={diurnalChartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                <XAxis dataKey="hour" tick={{ fontSize: 10, fill: '#94a3b8' }} interval={3} />
                <YAxis tick={{ fontSize: 10, fill: '#94a3b8' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderRadius: '8px', border: 'none', color: '#fff', fontSize: '11px' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px' }} />
                <Line type="monotone" dataKey="PM10" name="PM10 (µg/m³)" stroke="#f59e0b" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="PM25" name="PM2.5 (µg/m³)" stroke="#8b5cf6" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="NO2" name="NO2 (µg/m³)" stroke="#ec4899" strokeWidth={1.8} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-sky-50/60 rounded-xl p-3 border border-sky-100 text-xs text-sky-900 space-y-1">
            <div className="font-semibold text-sky-950 flex items-center gap-1.5">
              <Info className="w-3.5 h-3.5 text-sky-600" />
              <span>Descriptive Historical Patterns at {selectedDiurnalStation}</span>
            </div>
            <p className="text-[11px] text-sky-800 leading-relaxed">
              • NO2 exhibits peak elevation during morning transit hours (07:00–09:00).<br/>
              • PM10 and PM2.5 demonstrate secondary morning peaks and pronounced late evening elevations (20:00–23:00).<br/>
              • Lowest particulate concentrations historically occur during midday (12:00–16:00).
            </p>
            <p className="text-[10px] text-sky-600 italic pt-1 border-t border-sky-200/50">
              * Note: These are descriptive empirical observations from specific monitoring stations; not extrapolated citywide or claimed as universal medical advice.
            </p>
          </div>
        </div>

        {/* Retrospective Weather-Pollution Associations */}
        <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 space-y-4">
          <div>
            <div className="flex items-center gap-1.5">
              <Wind className="w-4 h-4 text-teal-600" />
              <h3 className="font-bold text-slate-900 text-base">Retrospective Weather Associations</h3>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">Pearson correlation coefficients (r) between meteorological features and pollutants</p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-100 text-[11px] uppercase tracking-wider text-slate-400">
                  <th className="py-2 font-semibold">Pollutant</th>
                  <th className="py-2 text-center font-semibold">Wind Speed</th>
                  <th className="py-2 text-center font-semibold">Precipitation</th>
                  <th className="py-2 text-center font-semibold">Rel. Humidity</th>
                  <th className="py-2 text-center font-semibold">Pressure</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50 font-mono">
                {[
                  { name: 'PM2.5', row: weatherImpact?.correlation_matrix?.pm25 },
                  { name: 'PM10', row: weatherImpact?.correlation_matrix?.pm10 },
                  { name: 'NO2', row: weatherImpact?.correlation_matrix?.no2 },
                  { name: 'SO2', row: weatherImpact?.correlation_matrix?.so2 },
                  { name: 'City AQI', row: weatherImpact?.correlation_matrix?.city_aqi },
                ].map((item) => (
                  <tr key={item.name} className="hover:bg-slate-50/60">
                    <td className="py-2.5 font-sans font-bold text-slate-800">{item.name}</td>
                    <td className={`py-2.5 text-center font-semibold ${item.row?.wind_speed_resultant && item.row.wind_speed_resultant < 0 ? 'text-teal-600' : 'text-slate-600'}`}>
                      {item.row?.wind_speed_resultant ?? '—'}
                    </td>
                    <td className={`py-2.5 text-center font-semibold ${item.row?.precipitation_sum && item.row.precipitation_sum < 0 ? 'text-sky-600' : 'text-slate-600'}`}>
                      {item.row?.precipitation_sum ?? '—'}
                    </td>
                    <td className={`py-2.5 text-center font-semibold ${item.row?.humidity_mean && item.row.humidity_mean < 0 ? 'text-indigo-600' : 'text-slate-600'}`}>
                      {item.row?.humidity_mean ?? '—'}
                    </td>
                    <td className={`py-2.5 text-center font-semibold ${item.row?.pressure_mean && item.row.pressure_mean > 0 ? 'text-rose-600' : 'text-slate-600'}`}>
                      {item.row?.pressure_mean ? `+${item.row.pressure_mean}` : '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="bg-slate-50 rounded-xl p-3 border border-slate-100 text-xs text-slate-700 space-y-1.5">
            <div className="font-semibold text-slate-900 flex items-center gap-1.5">
              <HelpCircle className="w-3.5 h-3.5 text-slate-500" />
              <span>Statistical Association Notes (Correlation ≠ Causation)</span>
            </div>
            <p className="text-[11px] text-slate-600 leading-relaxed">
              • <strong>Wind Speed (r = -0.263 vs PM2.5):</strong> Higher surface wind speed is historically associated with lower particulate accumulation.<br/>
              • <strong>Precipitation (r = -0.431 vs PM10):</strong> Rainfall days are historically associated with lower suspended coarse dust levels.<br/>
              • <strong>Surface Pressure (r = +0.607 vs City AQI):</strong> High atmospheric pressure in post-monsoon and winter months is historically associated with higher AQI.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
