import React, { useState } from 'react';
import {
  CitySummary,
  StationMeta
} from '../types';
import {
  Wind,
  Thermometer,
  Droplets,
  Gauge,
  MapPin,
  Clock,
  Compass,
  Search,
  Activity,
  AlertCircle,
  TrendingUp,
  CloudRain
} from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

interface OverviewViewProps {
  citySummary: CitySummary | null;
  stations: StationMeta[];
  loading: boolean;
}

export const OverviewView: React.FC<OverviewViewProps> = ({
  citySummary,
  stations,
  loading
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterActive, setFilterActive] = useState<'all' | 'active' | 'decommissioned'>('all');

  if (loading || !citySummary) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <div className="w-10 h-10 border-4 border-sky-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-sm font-medium text-slate-500">Loading Bengaluru Air Quality Data...</p>
      </div>
    );
  }

  const filteredStations = stations.filter((s) => {
    const matchesSearch = s.station_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          s.station_id.toLowerCase().includes(searchQuery.toLowerCase());
    if (filterActive === 'active') return matchesSearch && s.is_active;
    if (filterActive === 'decommissioned') return matchesSearch && !s.is_active;
    return matchesSearch;
  });

  const getCategoryBadgeClass = (category: string) => {
    switch (category) {
      case 'Good': return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'Satisfactory': return 'bg-lime-50 text-lime-700 border-lime-200';
      case 'Moderate': return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'Poor': return 'bg-orange-50 text-orange-700 border-orange-200';
      case 'Very Poor': return 'bg-red-50 text-red-700 border-red-200';
      case 'Severe': return 'bg-rose-100 text-rose-800 border-rose-300';
      default: return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  const getAQIColor = (aqi: number | null) => {
    if (aqi === null) return '#94a3b8';
    if (aqi <= 50) return '#10b981';
    if (aqi <= 100) return '#84cc16';
    if (aqi <= 200) return '#eab308';
    if (aqi <= 300) return '#f97316';
    if (aqi <= 400) return '#ef4444';
    return '#991b1b';
  };

  return (
    <div className="space-y-8">
      {/* Hero Historical Status Card */}
      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 sm:p-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-sky-50 to-teal-50 rounded-full blur-3xl -z-10 opacity-70"></div>

        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200">
                <Clock className="w-3.5 h-3.5 text-slate-500" />
                Latest Available Historical Record: {citySummary.latest_date}
              </span>
              <span className="text-xs text-amber-800 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded font-medium">
                Not Current Conditions
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              Bengaluru City Composite Air Quality
            </h1>
            <p className="text-sm text-slate-500 mt-1">
              Composite arithmetic mean derived from {citySummary.reporting_stations_count} CPCB & KSPCB active stations adhering to official CPCB Table 3.2 rules.
            </p>
          </div>

          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-xs uppercase tracking-wider font-semibold text-slate-400">Index Category</div>
              <div className={`mt-1 inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-bold border ${getCategoryBadgeClass(citySummary.category)}`}>
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: getAQIColor(citySummary.city_aqi) }}></span>
                {citySummary.category}
              </div>
            </div>

            <div className="p-4 rounded-2xl bg-slate-900 text-white min-w-[130px] text-center shadow-lg shadow-slate-900/10">
              <div className="text-[11px] font-medium text-slate-400 uppercase tracking-wider">City AQI</div>
              <div className="text-4xl font-extrabold tracking-tight mt-0.5" style={{ color: getAQIColor(citySummary.city_aqi) }}>
                {citySummary.city_aqi}
              </div>
              <div className="text-[10px] text-slate-400 mt-1 font-mono">
                Driver: <span className="text-white font-semibold">{citySummary.prominent_pollutant}</span>
              </div>
            </div>
          </div>
        </div>

        {/* 14-Day Trend Sparkline & Weather Strip */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 pt-6">
          <div className="lg:col-span-2">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-sky-600" />
                <span className="text-xs font-bold uppercase tracking-wider text-slate-600">14-Day Historical Trajectory (Oct 18 – Oct 31, 2024)</span>
              </div>
              <span className="text-xs text-slate-400 font-mono">Daily Composite AQI</span>
            </div>
            <div className="h-40 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={citySummary.sparkline_14d} margin={{ top: 5, right: 10, left: -25, bottom: 0 }}>
                  <defs>
                    <linearGradient id="aqiGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.4}/>
                      <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0.0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="date" tick={{ fontSize: 10, fill: '#94a3b8' }} tickFormatter={(d) => d.slice(5)} />
                  <YAxis domain={[40, 160]} tick={{ fontSize: 10, fill: '#94a3b8' }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderRadius: '8px', border: 'none', color: '#fff', fontSize: '12px' }}
                    labelStyle={{ color: '#94a3b8', fontSize: '11px', marginBottom: '2px' }}
                  />
                  <Area type="monotone" dataKey="city_aqi" name="City AQI" stroke="#0ea5e9" strokeWidth={2.5} fillOpacity={1} fill="url(#aqiGrad)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Meteorological Reanalysis Observations */}
          <div className="bg-slate-50/80 rounded-xl p-4 border border-slate-200/60 flex flex-col justify-between">
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">
              <Compass className="w-4 h-4 text-teal-600" />
              <span>ERA5 Meteorology (Oct 31, 2024)</span>
            </div>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="bg-white p-2.5 rounded-lg border border-slate-200/50">
                <div className="flex items-center gap-1.5 text-slate-400 text-[11px] mb-1">
                  <Thermometer className="w-3.5 h-3.5 text-rose-500" />
                  <span>Temperature</span>
                </div>
                <div className="font-bold text-slate-800 text-sm">{citySummary.weather.temp_mean}°C</div>
                <div className="text-[10px] text-slate-400">Min {citySummary.weather.temp_min}° / Max {citySummary.weather.temp_max}°</div>
              </div>

              <div className="bg-white p-2.5 rounded-lg border border-slate-200/50">
                <div className="flex items-center gap-1.5 text-slate-400 text-[11px] mb-1">
                  <Droplets className="w-3.5 h-3.5 text-sky-500" />
                  <span>Humidity</span>
                </div>
                <div className="font-bold text-slate-800 text-sm">{citySummary.weather.humidity_mean}%</div>
                <div className="text-[10px] text-slate-400">Daily Mean RH</div>
              </div>

              <div className="bg-white p-2.5 rounded-lg border border-slate-200/50">
                <div className="flex items-center gap-1.5 text-slate-400 text-[11px] mb-1">
                  <Wind className="w-3.5 h-3.5 text-teal-500" />
                  <span>Vector Wind</span>
                </div>
                <div className="font-bold text-slate-800 text-sm">{citySummary.weather.wind_speed_resultant} km/h</div>
                <div className="text-[10px] text-slate-400">{citySummary.weather.wind_dir_resultant}° Bearing</div>
              </div>

              <div className="bg-white p-2.5 rounded-lg border border-slate-200/50">
                <div className="flex items-center gap-1.5 text-slate-400 text-[11px] mb-1">
                  <Gauge className="w-3.5 h-3.5 text-indigo-500" />
                  <span>Pressure</span>
                </div>
                <div className="font-bold text-slate-800 text-sm">{citySummary.weather.pressure_mean} hPa</div>
                <div className="text-[10px] text-slate-400">Surface Pressure</div>
              </div>
            </div>
            <div className="mt-2 text-[10px] text-slate-400 flex items-center gap-1">
              <CloudRain className="w-3 h-3 text-sky-500" />
              <span>Precipitation: {citySummary.weather.precipitation_sum} mm</span>
            </div>
          </div>
        </div>

        {/* Criteria Pollutants Strip */}
        <div className="mt-6 pt-6 border-t border-slate-100">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
            Criteria Pollutant Concentrations (Daily Mean on Oct 31, 2024)
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
            {[
              { name: 'PM2.5', val: citySummary.concentrations['PM2.5'], unit: 'µg/m³', std: '60 (24h)' },
              { name: 'PM10', val: citySummary.concentrations['PM10'], unit: 'µg/m³', std: '100 (24h)' },
              { name: 'NO2', val: citySummary.concentrations['NO2'], unit: 'µg/m³', std: '80 (24h)' },
              { name: 'SO2', val: citySummary.concentrations['SO2'], unit: 'µg/m³', std: '80 (24h)' },
              { name: 'CO', val: citySummary.concentrations['CO'], unit: 'mg/m³', std: '2 (8h)' },
              { name: 'Ozone', val: citySummary.concentrations['Ozone'], unit: 'µg/m³', std: '100 (8h)' },
              { name: 'NH3', val: citySummary.concentrations['NH3'], unit: 'µg/m³', std: '400 (24h)' },
            ].map((p) => (
              <div key={p.name} className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                <div className="text-xs font-semibold text-slate-500 flex items-center justify-between">
                  <span>{p.name}</span>
                  <span className="text-[10px] text-slate-400">Std: {p.std}</span>
                </div>
                <div className="text-lg font-extrabold text-slate-900 mt-1">
                  {p.val !== null ? p.val : '—'} <span className="text-[10px] font-normal text-slate-400">{p.unit}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Monitoring Station Network Cards */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-slate-900">CAAQM Monitoring Station Network</h2>
            <p className="text-xs text-slate-500 mt-0.5">
              14 cataloged continuous monitoring stations in Bengaluru (13 active, 1 decommissioned).
            </p>
          </div>

          <div className="flex items-center gap-2">
            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Search station or location..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-9 pr-3 py-1.5 text-xs rounded-lg border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-sky-500 w-48 sm:w-64"
              />
            </div>

            <div className="flex items-center bg-white border border-slate-200 rounded-lg p-0.5 text-xs font-medium">
              <button
                onClick={() => setFilterActive('all')}
                className={`px-2.5 py-1 rounded-md transition ${filterActive === 'all' ? 'bg-sky-50 text-sky-700 font-bold' : 'text-slate-600'}`}
              >
                All (14)
              </button>
              <button
                onClick={() => setFilterActive('active')}
                className={`px-2.5 py-1 rounded-md transition ${filterActive === 'active' ? 'bg-sky-50 text-sky-700 font-bold' : 'text-slate-600'}`}
              >
                Active (13)
              </button>
              <button
                onClick={() => setFilterActive('decommissioned')}
                className={`px-2.5 py-1 rounded-md transition ${filterActive === 'decommissioned' ? 'bg-sky-50 text-sky-700 font-bold' : 'text-slate-600'}`}
              >
                Decommissioned (1)
              </button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredStations.map((st) => (
            <div
              key={st.station_id}
              className={`bg-white rounded-xl p-4 border transition-all ${
                st.is_active ? 'border-slate-200/80 hover:shadow-md hover:border-sky-300' : 'border-slate-200 bg-slate-50/50 opacity-75'
              }`}
            >
              <div className="flex items-start justify-between gap-2 mb-2">
                <div>
                  <span className="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-wider">{st.station_id}</span>
                  <h3 className="font-bold text-sm text-slate-900 leading-snug line-clamp-1">{st.station_name}</h3>
                </div>
                {st.is_active ? (
                  <span className="shrink-0 text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                    Active
                  </span>
                ) : (
                  <span className="shrink-0 text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-200 text-slate-700">
                    Closed Aug 2022
                  </span>
                )}
              </div>

              <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-3">
                <MapPin className="w-3.5 h-3.5 text-slate-400" />
                <span>{st.latitude?.toFixed(4)}, {st.longitude?.toFixed(4)}</span>
              </div>

              {st.is_active ? (
                <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                  <div>
                    <div className="text-[10px] uppercase tracking-wider text-slate-400 font-medium">Historical AQI</div>
                    <div className="text-xl font-extrabold" style={{ color: getAQIColor(st.latest_aqi || null) }}>
                      {st.latest_aqi !== null && st.latest_aqi !== undefined ? st.latest_aqi : 'N/A'}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`text-[11px] font-bold px-2 py-0.5 rounded border ${getCategoryBadgeClass(st.latest_category || 'Unknown')}`}>
                      {st.latest_category}
                    </div>
                    <div className="text-[10px] text-slate-400 mt-1 font-mono">
                      Driver: <span className="font-semibold text-slate-700">{st.latest_prominent || 'None'}</span>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="pt-3 border-t border-slate-200/60 text-xs text-slate-500 flex items-center gap-1.5">
                  <AlertCircle className="w-4 h-4 text-slate-400 shrink-0" />
                  <span>BWSSB Kadabesanahalli decommissioned before 2023.</span>
                </div>
              )}

              <div className="mt-3 pt-2 border-t border-slate-50 flex items-center justify-between text-[11px] text-slate-400">
                <span>Coverage: {st.valid_aqi_days_count} valid days</span>
                <span className="font-mono text-[10px]">{st.monitored_parameters.length} criteria</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
