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

// -------------------------------------------------------------
// BreatheWise AI Expansion Interfaces (Phases B, C, D)
// -------------------------------------------------------------

export interface PollutantStatusItem {
  name: string;
  display_name: string;
  concentration: number | null;
  unit: string;
  averaging_period: string;
  sub_index: number | null;
  tier: string;
  is_valid: boolean;
  is_informational: boolean;
  notes?: string | null;
}

export interface MeteorologyContextItem {
  temperature_mean: number | null;
  temp_min: number | null;
  temp_max: number | null;
  humidity_mean: number | null;
  wind_speed_resultant: number | null;
  wind_dir_resultant: number | null;
  wind_u: number | null;
  wind_v: number | null;
  precipitation_sum: number | null;
  pressure_mean: number | null;
}

export interface CorrelationItem {
  metric_x: string;
  metric_y: string;
  pearson_r: number;
  spearman_rho?: number;
  n_samples: number;
  p_value?: number;
  scope: string;
  scope_note?: string | null;
  description: string;
}

export interface EnvironmentalInsightsResponse {
  status: string;
  date: string;
  is_historical: boolean;
  station: {
    id: string;
    name: string;
    active_stations_count?: number;
    latitude?: number | null;
    longitude?: number | null;
    is_active: boolean;
    status?: string;
    message?: string | null;
  };
  aqi_summary: {
    aqi: number | null;
    category: string;
    prominent_pollutant: string | null;
    category_meta?: any;
  };
  pollutants: PollutantStatusItem[];
  meteorology: MeteorologyContextItem;
  correlation_scope: string;
  correlations: CorrelationItem[];
  data_integrity?: any;
  disclaimer: string;
}

export interface DiagnosticMetrics {
  n_samples: number;
  feature_dim: number;
  k_evaluated: number[];
  optimal_k: number;
  silhouette_score: number;
  min_cluster_size_pct: number;
  cluster_inertia: number;
  cluster_sizes: number[];
  multi_seed_stability_ari: number;
}

export interface AcceptanceHeuristic {
  silhouette_threshold: number;
  silhouette_passed: boolean;
  min_cluster_ratio: number;
  min_cluster_ratio_passed: boolean;
  all_passed: boolean;
}

export interface RegimeQuantiles {
  p0: number;
  p25: number;
  p50: number;
  p75: number;
  p100: number;
}

export interface RegimeProfileItem {
  cluster_id: number;
  name: string;
  description: string;
  sample_count: number;
  sample_percentage: number;
  dominant_months: string;
  centroid: {
    pm25: number;
    pm10: number;
    no2: number;
    temp_mean: number;
    humidity_mean: number;
    wind_u: number;
    wind_v: number;
    pressure_mean: number;
  };
  mean_aqi: number;
  mean_category: string;
  quantiles?: Record<string, RegimeQuantiles> | null;
}

export interface EnvironmentalRegimesResponse {
  status: string;
  is_fallback: boolean;
  fallback_reason?: string | null;
  diagnostic_metrics: DiagnosticMetrics;
  acceptance_heuristic: AcceptanceHeuristic;
  regimes: RegimeProfileItem[];
  disclaimer: string;
}

export interface SensitiveGroupAdvice {
  asthma: string;
  elderly_and_children: string;
  outdoor_workers: string;
}

export interface TriggeredAdvisoryItem {
  rule_id: string;
  category: string;
  trigger_metric: string;
  trigger_value: number;
  general_public_advice: string;
  sensitive_groups_advice: SensitiveGroupAdvice;
  outdoor_activity_recommendation: string;
}

export interface HealthAdvisoryResponse {
  status: string;
  evaluation_date?: string | null;
  station_id?: string | null;
  is_hypothetical: boolean;
  aqi: number;
  category: string;
  prominent_pollutant?: string | null;
  advisories: TriggeredAdvisoryItem[];
  medical_disclaimer: string;
}

export interface DecayPoint {
  time_hours: number;
  pm25_ug_m3: number;
  reduction_pct: number;
}

export interface PurificationSimulationRequest {
  room_area_m2: number;
  ceiling_height_m: number;
  initial_pm25_ug_m3: number;
  cadr_m3_h: number;
  runtime_hours: number;
}

export interface PurificationSimulationResponse {
  status: string;
  room_area_m2: number;
  ceiling_height_m: number;
  room_volume_m3: number;
  initial_pm25_ug_m3: number;
  initial_pm25_source: string;
  cadr_m3_h: number;
  runtime_hours: number;
  air_changes_per_hour_cadr: number;
  final_pm25_ug_m3: number;
  percentage_reduction: number;
  decay_curve: DecayPoint[];
  formula_used: string;
  assumptions_ledger: string[];
  disclaimer: string;
}
