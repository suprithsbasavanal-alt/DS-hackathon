export interface CategoryMeta {
  name: string;
  min: number;
  max: number;
  color: string;
  badge: string;
  desc: string;
}

export interface CitySummary {
  city: string;
  latest_date: string;
  city_aqi: number;
  category: string;
  category_meta: CategoryMeta;
  prominent_pollutant: string;
  reporting_stations_count: number;
  concentrations: {
    'PM2.5': number | null;
    'PM10': number | null;
    'NO2': number | null;
    'SO2': number | null;
    'CO': number | null;
    'Ozone': number | null;
    'NH3': number | null;
  };
  weather: {
    temp_mean: number | null;
    temp_min: number | null;
    temp_max: number | null;
    humidity_mean: number | null;
    precipitation_sum: number | null;
    wind_speed_resultant: number | null;
    wind_dir_resultant: number | null;
    pressure_mean: number | null;
  };
  sparkline_14d: Array<{
    date: string;
    city_aqi: number;
    category: string;
  }>;
}

export interface StationMeta {
  station_id: string;
  station_name: string;
  city: string;
  state: string;
  latitude: number;
  longitude: number;
  is_active: boolean;
  reporting_days_count: number;
  valid_aqi_days_count: number;
  monitored_parameters: string[];
  latest_aqi?: number | null;
  latest_category?: string;
  latest_category_meta?: CategoryMeta;
  latest_prominent?: string | null;
  latest_date?: string | null;
}

export interface TrendRecord {
  date: string;
  city_aqi: number | null;
  category: string;
  prominent_pollutant: string | null;
  reporting_stations_count: number;
  pm25: number | null;
  pm10: number | null;
  no2: number | null;
  so2: number | null;
  co: number | null;
  o3: number | null;
  nh3: number | null;
  temp_mean: number | null;
  humidity_mean: number | null;
  precipitation_sum: number | null;
  wind_speed_resultant: number | null;
  wind_dir_resultant: number | null;
  pressure_mean: number | null;
}

export interface WeatherImpact {
  correlation_matrix: {
    [pollutant: string]: {
      [weatherVar: string]: number | null;
    };
  };
  key_findings: Array<{
    pair: string;
    correlation: number | null;
    direction: string;
    insight: string;
  }>;
}

export interface DiurnalPoint {
  hour: number;
  mean_concentration: number | null;
  sample_count: number;
}

export interface DiurnalData {
  [stationName: string]: {
    station_id: string;
    diurnal_curves: {
      [parameter: string]: DiurnalPoint[];
    };
    sampling_scope: string;
    notes: string;
  };
}

export interface ModelMetric {
  model_name: string;
  description: string;
  mae: number;
  rmse: number;
  r2: number;
  mape: number;
}

export interface ForecastBacktest {
  evaluation_protocol: {
    split_type: string;
    train_period: string;
    test_period: string;
    train_samples_count: number;
    test_samples_count: number;
    target_variable: string;
    anti_leakage_guarantee: string;
  };
  scientific_reconciliation_note: string;
  model_comparison: ModelMetric[];
  top_features: Array<{
    feature: string;
    importance: number;
    label: string;
  }>;
  test_timeline: Array<{
    target_date: string;
    actual_aqi: number;
    persistence_pred: number;
    direct_rf_pred: number;
    physical_derived_pred: number;
    moving_avg_pred: number;
  }>;
}

export interface TransparencyLedger {
  data_provenance: {
    air_quality_source: string;
    weather_source: string;
    city: string;
    temporal_range: string;
    air_quality_license: string;
    weather_license: string;
    genuine_data_verification: string;
  };
  audit_metrics: {
    total_raw_daily_records: number;
    cpcb_16hour_sufficiency_filtered_out: number;
    duplicate_records_dropped: number;
    compliant_daily_records_preserved: number;
    cataloged_stations_count: number;
    active_monitoring_stations_count: number;
    decommissioned_stations: string[];
    total_hourly_weather_records: number;
    landmark_hourly_seasonal_observations: number;
  };
  regulatory_compliance_notes: string[];
}
