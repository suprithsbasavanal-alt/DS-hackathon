import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { OverviewView } from './views/OverviewView';
import { ExplorerView } from './views/ExplorerView';
import { ForecastArenaView } from './views/ForecastArenaView';
import { HealthAdvisoryView } from './views/HealthAdvisoryView';
import { DataTransparencyView } from './views/DataTransparencyView';
import { AIInsightsView } from './views/AIInsightsView';

import {
  fetchCitySummary,
  fetchStations,
  fetchTrends,
  fetchWeatherImpact,
  fetchDiurnalData,
  fetchForecastBacktest,
  fetchTransparency
} from './services/api';

import {
  CitySummary,
  StationMeta,
  TrendRecord,
  WeatherImpact,
  DiurnalData,
  ForecastBacktest,
  TransparencyLedger
} from './types';
import { AlertCircle, RefreshCw } from 'lucide-react';

export const App: React.FC = () => {
  const getInitialTab = () => {
    const hash = window.location.hash.replace('#', '');
    if (['overview', 'explorer', 'forecast', 'ai-insights', 'health', 'transparency'].includes(hash)) {
      return hash;
    }
    return 'overview';
  };

  const [activeTab, setActiveTabState] = useState<string>(getInitialTab);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const setActiveTab = (tab: string) => {
    setActiveTabState(tab);
    window.location.hash = tab;
  };

  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.replace('#', '');
      if (['overview', 'explorer', 'forecast', 'ai-insights', 'health', 'transparency'].includes(hash)) {
        setActiveTabState(hash);
      }
    };
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const [citySummary, setCitySummary] = useState<CitySummary | null>(null);
  const [stations, setStations] = useState<StationMeta[]>([]);
  const [trends, setTrends] = useState<TrendRecord[]>([]);
  const [weatherImpact, setWeatherImpact] = useState<WeatherImpact | null>(null);
  const [diurnalData, setDiurnalData] = useState<DiurnalData | null>(null);
  const [forecastData, setForecastData] = useState<ForecastBacktest | null>(null);
  const [transparencyData, setTransparencyData] = useState<TransparencyLedger | null>(null);

  const loadAllData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [cityRes, stationsRes, trendsRes, weatherRes, diurnalRes, forecastRes, transparencyRes] =
        await Promise.all([
          fetchCitySummary(),
          fetchStations(),
          fetchTrends(),
          fetchWeatherImpact(),
          fetchDiurnalData(),
          fetchForecastBacktest(),
          fetchTransparency()
        ]);

      setCitySummary(cityRes);
      setStations(stationsRes);
      setTrends(trendsRes);
      setWeatherImpact(weatherRes);
      setDiurnalData(diurnalRes);
      setForecastData(forecastRes);
      setTransparencyData(transparencyRes);
    } catch (err: any) {
      console.error('Error loading BreatheWise data:', err);
      setError(err?.message || 'Failed to load air quality data from local API.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans">
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        latestDate={citySummary?.latest_date}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error ? (
          <div className="bg-red-50 border border-red-200 rounded-2xl p-6 text-red-900 space-y-4">
            <div className="flex items-center gap-2 font-bold text-base text-red-950">
              <AlertCircle className="w-5 h-5 text-red-600 shrink-0" />
              <span>Unable to connect to local BreatheWise API</span>
            </div>
            <p className="text-xs text-red-800 leading-relaxed font-mono">
              {error}
            </p>
            <p className="text-xs text-red-700">
              Please ensure the FastAPI backend is running on <code>http://localhost:8000</code>.
            </p>
            <button
              onClick={loadAllData}
              className="inline-flex items-center gap-1.5 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl text-xs font-semibold transition"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Retry Connection
            </button>
          </div>
        ) : (
          <>
            {activeTab === 'overview' && (
              <OverviewView
                citySummary={citySummary}
                stations={stations}
                loading={loading}
              />
            )}
            {activeTab === 'explorer' && (
              <ExplorerView
                trends={trends}
                weatherImpact={weatherImpact}
                diurnalData={diurnalData}
                loading={loading}
              />
            )}
            {activeTab === 'forecast' && (
              <ForecastArenaView
                forecastData={forecastData}
                loading={loading}
              />
            )}
            {activeTab === 'ai-insights' && (
              <AIInsightsView
                stations={stations}
              />
            )}
            {activeTab === 'health' && (
              <HealthAdvisoryView
                currentAqi={citySummary?.city_aqi}
                currentCategory={citySummary?.category}
                diurnalData={diurnalData}
              />
            )}
            {activeTab === 'transparency' && (
              <DataTransparencyView
                transparencyData={transparencyData}
                loading={loading}
              />
            )}
          </>
        )}
      </main>

      <Footer />
    </div>
  );
};

export default App;
