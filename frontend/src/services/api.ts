import {
  CitySummary,
  StationMeta,
  TrendRecord,
  WeatherImpact,
  DiurnalData,
  ForecastBacktest,
  TransparencyLedger
} from '../types';

const API_BASE = '/api';

export async function fetchCitySummary(): Promise<CitySummary> {
  const res = await fetch(`${API_BASE}/city/summary`);
  if (!res.ok) throw new Error(`Failed to fetch city summary: ${res.statusText}`);
  return res.json();
}

export async function fetchStations(): Promise<StationMeta[]> {
  const res = await fetch(`${API_BASE}/stations`);
  if (!res.ok) throw new Error(`Failed to fetch stations: ${res.statusText}`);
  return res.json();
}

export async function fetchTrends(startDate?: string, endDate?: string): Promise<TrendRecord[]> {
  const params = new URLSearchParams();
  if (startDate) params.append('start_date', startDate);
  if (endDate) params.append('end_date', endDate);
  const url = `${API_BASE}/analytics/trends${params.toString() ? `?${params.toString()}` : ''}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch trends: ${res.statusText}`);
  return res.json();
}

export async function fetchWeatherImpact(): Promise<WeatherImpact> {
  const res = await fetch(`${API_BASE}/analytics/weather-impact`);
  if (!res.ok) throw new Error(`Failed to fetch weather impact: ${res.statusText}`);
  return res.json();
}

export async function fetchDiurnalData(): Promise<DiurnalData> {
  const res = await fetch(`${API_BASE}/analytics/diurnal`);
  if (!res.ok) throw new Error(`Failed to fetch diurnal profiles: ${res.statusText}`);
  return res.json();
}

export async function fetchForecastBacktest(): Promise<ForecastBacktest> {
  const res = await fetch(`${API_BASE}/forecast/backtest`);
  if (!res.ok) throw new Error(`Failed to fetch forecast backtest: ${res.statusText}`);
  return res.json();
}

export async function fetchTransparency(): Promise<TransparencyLedger> {
  const res = await fetch(`${API_BASE}/transparency`);
  if (!res.ok) throw new Error(`Failed to fetch transparency metrics: ${res.statusText}`);
  return res.json();
}
