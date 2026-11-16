# SPEC.md — BreatheWise Complete AI Expansion Specification

> **Status**: `FINALIZED`  
> **Milestone**: Complete AI Environmental Intelligence & Decision Support Expansion  
> **Scope**: Backend Intelligence Modules, Typed REST Endpoints, AI Insights View, and Physics-Based Air Purification Simulator  
> **Author**: Antigravity Full-Stack Data Science Agent  
> **Review Framework**: Google Elephant-Goldfish Model (EGM) Architecture Standards  
> 
> ⚠️ **Planning Lock**: In accordance with `PROJECT_RULES.md`, this specification is finalized and locked for planning. Implementation code changes require explicit user authorization.

---

## 1. Vision & Core Philosophy

BreatheWise is an offline-first Data Science platform coupling genuine Central Pollution Control Board (CPCB) continuous monitoring data with ECMWF ERA5 atmospheric reanalysis across Bengaluru, Karnataka, India.

The **Complete AI Expansion** extends BreatheWise beyond retrospective dashboarding into explainable environmental intelligence and transparent physics-based decision support. In strict adherence to scientific integrity:
1. **Zero Black-Box Claims:** Statistical associations are never framed as physical causation; feature importance is never claimed as causal attribution.
2. **Deterministic Regulatory Integrity:** Health advice is deterministically mapped to official CPCB Table 3.2 AQI tiers and valid pollutant thresholds with auditable rule IDs.
3. **Physics vs. AI Demarcation:** The indoor air purification simulator is explicitly formulated as an idealized first-order mass-balance physics equation—**never an AI model**, never a measured sensor reading, and never a commercial purifier efficacy endorsement.
4. **Transparent Machine Learning:** Unsupervised environmental regimes include rigorous silhouette and cluster stability diagnostics with an automated fallback to descriptive quantile grouping if stability criteria fail.
5. **Baselines & Leakage Prevention:** The existing 4-model forecasting benchmark (Persistence MAE 7.42 vs Direct RF 7.74 vs Two-Stage Physical 7.91) is maintained on chronological held-out splits with zero future weather leakage.

---

## 2. Hard Scientific Boundaries (Non-Negotiable)

1. **Raw Data Preservation:** The raw files in `data/raw/` (`bengaluru_daily_combined_raw.json`, `bengaluru_weather_openmeteo.json`, `hourly_*.json`) are immutable and remain strictly untouched. All derived artifacts in `data/processed/` must be 100% reproducible.
2. **Historical Temporal Boundary:** Ground-truth observations conclude on **October 31, 2024**. They must never be labeled as "current conditions", real-time data, or a live forecast for 2026.
3. **Daily CO and $\text{O}_3$ Averaging Period Rule:** Harvested daily records represent 24-hour arithmetic daily means. In accordance with CPCB guidelines (which require 8-hour rolling averages), daily CO and $\text{O}_3$ must **never** be used as CPCB 8-hour metrics or included in daily station AQI calculations.
4. **Hourly CO/$\text{O}_3$ 8-Hour Benchmark Restriction:** Genuine 8-hour rolling averages are evaluated exclusively on authentic landmark hourly observations (BTM Layout and Peenya across Jan, Apr, Jul, Oct 2024). The project-defined $\ge 6$ of 8 valid hours (75%) completeness rule is maintained and explicitly labeled as a project quality threshold.
5. **CPCB Station AQI Constraints:** Daily station AQI requires $\ge 16$ valid hours per pollutant, $\ge 3$ valid criteria pollutants including at least one particulate matter ($\text{PM}_{2.5}$ or $\text{PM}_{10}$), and the worst-pollutant principle ($\text{AQI} = \max_p I_p$). The Severe category 500 ceiling cap is retained and explicitly documented as a project implementation policy, not an official CPCB interpolation formula.
6. **Lead (Pb) Absence:** Lead (Pb) is not present in the CAAQM dataset. Pb is never fabricated, imputed, or assumed zero. It must be explicitly rendered as `"Not available in supplied dataset"`.
7. **Weather vs. Regulatory Breakpoints:** CPCB Table 3.2 breakpoints apply exclusively to criteria pollutants. Meteorological variables (temperature, relative humidity, wind speed, resultant vector direction, precipitation, surface pressure) have **zero regulatory or medical thresholds**. They must be described using historical empirical percentiles and clearly labeled descriptive bands.
8. **Correlation vs. Causation:** All Pearson/Spearman correlations, regression coefficients, and model feature importances represent observational statistical associations and model behavior. Non-causal language is strictly enforced throughout.
9. **Sample Size & Model Overparameterization:** The city composite daily dataset contains 670 calendar days. Complex, over-parameterized neural networks or ungrounded generative models are prohibited. Clustering models must be evaluated for stability ($k \in [2, 5]$); if silhouette $< 0.30$ or cluster assignments are unstable across random seeds, the system falls back to descriptive quantile groupings.
10. **Indoor Air & Purifier Reality:** The dataset contains zero indoor PM measurements, room dimensions, ventilation rates, or purifier CADR test logs. The purification simulator is strictly a user-parameterized theoretical what-if scenario based on the well-mixed mass-balance equation $C(t) = C_0 \times \exp\left(-\frac{\text{CADR}}{V} \times t\right)$.

---

## 3. Product Scope & Functional Requirements

The platform maintains the existing five production views (`Overview`, `Explorer`, `Forecast Arena`, `Health Advisory`, `Data Transparency`) and introduces:
1. **AI Insights Screen (`#ai-insights` / `AIInsightsView.tsx`):** Unified environmental intelligence synthesizing multi-pollutant threshold assessments, weather association matrices, exploratory environmental regimes with diagnostic fallbacks, and rule-based health advisories with trigger evidence.
2. **Physics-Based Air Purification Simulator Panel (`PurificationSimulator.tsx`):** A dedicated, interactive simulation tool accessible from both AI Insights and Health Advisory, computing theoretical clean-air decay curves with visible mathematical formulations and boundary validations.

### Feature Decomposition

#### A. Unified Environmental Analysis
- **Inputs:** 7 criteria pollutants ($\text{PM}_{2.5}, \text{PM}_{10}, \text{NO}_2, \text{SO}_2, \text{CO}, \text{O}_3, \text{NH}_3$), 6 meteorological parameters (temperature, relative humidity, precipitation, resultant wind speed, resultant wind direction, surface pressure), station selector (13 active stations + city composite), and date range filter.
- **Outputs:**
  - Historical freshness banner (latest date: 2024-10-31).
  - Multi-pollutant status table displaying observed concentration, unit, valid averaging period, data source, validity status, and CPCB threshold tier.
  - Dominant pollutant and station/city AQI computed via existing `cpcb_calculator.py`.
  - Missingness and coverage metadata badges for every metric.

#### B. Pollutant Threshold Assessment
- Reuse `backend/cpcb_calculator.py` directly (zero duplicated breakpoint tables).
- Validate input units ($\mu\text{g/m}^3$ for particulates and gases; $\text{mg/m}^3$ for CO).
- Daily pollutants evaluated against 24h breakpoints; CO/$\text{O}_3$ evaluated against 8h breakpoints on hourly landmark data only.
- Render Pb as `"Not available in supplied dataset"`.

#### C. Weather & Environmental Pattern Analysis
- Compute Pearson and Spearman correlation matrices with exact sample counts ($N$).
- Angular-safe wind vector handling: orthogonal decomposition into zonal ($u$) and meridional ($v$) components.
- Exploratory Environmental Regimes:
  - Feature set: $d=8$ standardized features: $\text{PM}_{2.5}$, $\text{PM}_{10}$, $\text{NO}_2$, temperature, humidity, wind zonal vector $u$, wind meridional vector $v$, and surface pressure ($N=670$ complete daily observations, verified 0.00% missingness). Scalar wind speed is deliberately excluded to prevent double-weighting wind in Euclidean distance since $\text{WindSpeed} = \sqrt{u^2 + v^2}$.
  - Algorithm: Standardized $k$-Means with cluster count $k \in [2, 5]$ evaluated via Mean Silhouette Score, inertia, and cluster size distribution.
  - Acceptance Heuristic & Stability Gate: The silhouette threshold ($S \ge 0.30$) is an analytical project acceptance heuristic, not scientific proof of physical cluster structure. If $S < 0.30$ or any cluster contains $< 5\%$ of dataset ($< 33$ days), the system automatically flags `is_fallback: true` and presents transparent seasonal quantile groupings. Multi-seed stability is verified using pairwise Adjusted Rand Index (ARI).
  - Model Card: Fully documented model card including feature weights, cluster centroids, sizes, inertia, multi-seed ARI stability, and non-causal interpretation.

#### D. Deterministic Health Advisory Engine
- Rule-based decision engine mapping CPCB Table 3.2 AQI categories (Good, Satisfactory, Moderate, Poor, Very Poor, Severe) and specific pollutant thresholds to actionable citizen guidance.
- Advisory outputs include:
  - `rule_id`: Unique identifier (e.g., `RULE-AQI-MOD-01`, `RULE-PM25-ELEV-02`).
  - `trigger_metric`: The exact metric triggering the advisory (e.g., `"City AQI: 141 (Moderate)"`, `"PM10: 133.3 µg/m³"`).
  - `general_public_advice`: Standard guidance for healthy individuals.
  - `sensitive_groups_advice`: Tailored safeguards for asthmatics, children, elderly, and outdoor workers.
  - `scope`: Geographic and temporal scope (e.g., `"Citywide Daily Composite • 2024-10-31"`).
  - `disclaimer`: Prominent statement that advice is general public health information, not medical diagnosis or prescription.

#### E. Hypothetical Air Purification Simulator
- **Mathematical Model:** Idealized first-order decay under well-mixed assumption:
  $$V = A \times h \quad (\text{m}^3)$$
  $$C(t) = C_0 \times \exp\left(-\frac{\text{CADR}}{V} \times t\right) \quad (\mu\text{g/m}^3)$$
  $$\text{Percentage Reduction} = \left(1 - \frac{C(t)}{C_0}\right) \times 100\%$$
- **Validated User Inputs:**
  - Room floor area $A \in [5, 200]\ \text{m}^2$ (default: $20\ \text{m}^2$)
  - Ceiling height $h \in [2.0, 5.0]\ \text{m}$ (default: $2.8\ \text{m}$)
  - Initial indoor $\text{PM}_{2.5}$ concentration $C_0 \in [5, 1000]\ \mu\text{g/m}^3$ (default: $67.7\ \mu\text{g/m}^3$, explicitly labeled as initialized from outdoor city composite observation in the absence of indoor sensors)
  - Purifier Clean Air Delivery Rate $\text{CADR} \in [0.0, 1200.0]\ \text{m}^3/\text{h}$ (default: $300\ \text{m}^3/\text{h}$; CADR=0 supported for pre-operation baseline)
  - Runtime $t \in [0.0, 12.0]\ \text{hours}$ (default: $2.0\ \text{hours}$; t=0 supported for instantaneous initial state)
- **Safety & Boundary Checks:**
  - $V \le 0 \implies \text{ValidationError}$
  - $t = 0 \implies C(t) = C_0, \text{Reduction} = 0\%$
  - $\text{CADR} = 0 \implies C(t) = C_0, \text{Reduction} = 0\%$
  - As $t \to \infty, C(t) \to 0$ monotonically.
- **Mandatory UI Disclosures & Expanded Assumptions:**
  - Clear banner: *"Hypothetical Physics Calculation • User-Entered Assumptions • Not an AI Model • Not an Indoor Sensor Reading"*.
  - Explicit assumption ledger:
    1. Instantaneous and perfect spatial mixing (no dead zones or localized concentration gradients).
    2. Zero continuing indoor emission sources (no cooking, smoking, incense, or dust resuspension).
    3. Zero infiltration of outdoor pollutants through doors, windows, and building envelope cracks.
    4. Zero natural particle deposition, gravitational settling, or wall loss.
    5. Continuous purifier operation at rated CADR without filter degradation, bypass, or airflow reduction.

---

## 4. Technical Architecture & Module Structure

```
backend/
├── cpcb_calculator.py           # Existing CPCB Table 3.2 logic (preserved)
├── data_pipeline.py             # Existing data pipeline & audit (preserved)
├── ml_pipeline.py               # Existing 4-model forecasting benchmark (preserved)
├── main.py                      # FastAPI app (extended with new routes)
├── schemas/                     # Pydantic v2 validation contracts
│   ├── __init__.py
│   ├── environmental.py         # Schemas for multi-pollutant & weather insights
│   ├── regimes.py               # Schemas for clustering & diagnostic fallback
│   ├── health.py                # Schemas for rule-based advisory & triggers
│   └── purification.py          # Schemas for room physics simulation
├── threshold_engine.py          # Thin adapter to cpcb_calculator with unit checks
├── environmental_analysis.py    # Unified pollutant summaries & correlation matrices
├── environmental_regimes.py     # Unsupervised clustering with silhouette & fallback
├── health_advisor.py            # Deterministic CPCB advisory engine with rule IDs
├── purification_simulator.py    # Validated first-order room CADR decay engine
├── test_cpcb_calculator.py      # Existing tests (43 passed)
├── test_data_pipeline.py        # Existing tests (8 passed)
├── test_api.py                  # Existing API tests (9 passed)
├── test_environmental.py        # NEW: Threshold adapter & analysis unit tests
├── test_regimes.py              # NEW: Cluster stability & fallback tests
├── test_health_advisor.py       # NEW: Rule ID & trigger evidence tests
└── test_purification.py         # NEW: Physics formula & boundary condition tests
```

---

## 5. API Contracts & Endpoint Specifications

### 1. `GET /api/ai/insights`
- **Query Params:** `station_id` (optional, default `"city_composite"`), `date` (optional, default `"2024-10-31"`)
- **Station Validation:**
  - Unknown station ID $\implies$ HTTP 404 Not Found.
  - Decommissioned station (`site_164`) $\implies$ structured response: `{"station_id": "site_164", "is_active": false, "status": "decommissioned", "message": "Station decommissioned August 2022. No observations in active 2023–2024 dataset."}`.
- **Response Schema (`EnvironmentalInsightsResponse`):**
  - `status`: `"success"`
  - `date`: `"2024-10-31"`
  - `is_historical`: `true`
  - `station`: `{"id": "city_composite", "name": "Bengaluru City Composite", "active_stations_count": 13}`
  - `aqi_summary`: `{"aqi": 141, "category": "Moderate", "prominent_pollutant": "PM10"}`
  - `pollutants`: Array of 7 criteria pollutants + Pb:
    - 24-hour criteria pollutants ($\text{PM}_{2.5}, \text{PM}_{10}, \text{NO}_2, \text{SO}_2, \text{NH}_3$): computed sub-index and official CPCB Table 3.2 tier.
    - Daily CO & $\text{O}_3$: evaluated from 24h arithmetic daily means; regulatory sub-index is strictly `null`, tier is `"CPCB 8h standard only"`, `is_valid: false`, `is_informational: true`.
    - Lead ($\text{Pb}$): `concentration: null`, `sub_index: null`, `tier: "Not available in supplied dataset"`, `is_valid: false`, `source: "Not monitored"`.
  - `meteorology`: `{"temperature_mean": 22.54, "humidity_mean": 82.83, "wind_speed_resultant": 4.61, "wind_dir_resultant": 109.4, "precipitation_sum": 4.0, "pressure_mean": 912.59}`
  - `correlations`: Array of correlation pairs with sample counts ($N=670$) and non-causal descriptor.

### 2. `GET /api/ai/regimes`
- **Response Mechanism:** Serves cached, precomputed JSON artifact `data/processed/environmental_regimes.json` for sub-millisecond offline performance.
- **Response Schema (`EnvironmentalRegimesResponse`):**
  - `is_fallback`: `boolean` (true if clustering fails stability criteria)
  - `diagnostic_metrics`: `{"n_samples": 670, "feature_dim": 8, "k_evaluated": [2, 3, 4, 5], "optimal_k": 3, "silhouette_score": 0.3557, "min_cluster_size_pct": 19.40, "cluster_inertia": 2601.0, "cluster_sizes": [338, 130, 202], "multi_seed_stability_ari": 1.0000}`
  - `acceptance_heuristic`: `{"min_silhouette": 0.30, "min_cluster_size_pct": 5.0, "status": "heuristic_passed", "note": "Project-defined analytical acceptance heuristic, not physical proof of cluster reality."}`
  - `regimes`: Array of cluster/group profiles with centroid characteristics, sample counts, seasonal distribution, and descriptive narrative (strictly descriptive observational labels: *"Monsoon and high-ventilation pattern"*, *"Hot/dry summer-transition pattern"*, *"Winter/post-monsoon pattern"*; never presented as proven pollution sources or atmospheric causes).
  - `disclaimer`: *"Exploratory atmospheric groupings based on standardized observations. Does not establish pollutant source attribution or physical causation."*

### 3. `GET /api/ai/health-advisory`
- **Query Params:** `aqi` (optional, float), `station_id` (optional), `date` (optional)
- **Query Semantics:**
  - If `aqi` query parameter is provided: evaluates a hypothetical advisory scenario (`is_hypothetical: true`, `station_id: null`, `date: null`).
  - If `aqi` is omitted: evaluates observed historical AQI for `station_id` (default `"city_composite"`) at `date` (default `"2024-10-31"`), with `is_hypothetical: false`.
- **Response Schema (`HealthAdvisoryResponse`):**
  - `evaluation_date`: `"2024-10-31"` (or null if hypothetical)
  - `station_id`: `"city_composite"` (or null if hypothetical)
  - `is_hypothetical`: `boolean`
  - `aqi`: `141`
  - `category`: `"Moderate"`
  - `prominent_pollutant`: `"PM10"`
  - `advisories`: Array of triggered advisories based on the deterministic catalog:
    - `RULE-AQI-GOOD-01` (0–50): Minimal impact; outdoor activities encouraged.
    - `RULE-AQI-SAT-01` (51–100): Minor breathing discomfort to sensitive people.
    - `RULE-AQI-MOD-01` (101–200): Breathing discomfort to people with asthma and heart disease.
    - `RULE-AQI-POOR-01` (201–300): Breathing discomfort to most people on prolonged exposure.
    - `RULE-AQI-VPOOR-01` (301–400): Respiratory illness on prolonged exposure.
    - `RULE-AQI-SEV-01` (401–500): Severe health impact even on healthy people; physical exertion avoided.
    - `RULE-PM25-ELEV-01` ($\text{PM}_{2.5} > 60\ \mu\text{g/m}^3$): Sensitive groups advisory.
    - `RULE-PM10-ELEV-01` ($\text{PM}_{10} > 100\ \mu\text{g/m}^3$): Coarse dust advisory.
  - `medical_disclaimer`: *"General public health information based on CPCB guidance. Not individualized medical advice."*

### 4. `POST /api/purification/simulate`
- **Request Body (`PurificationSimulationRequest`):**
  - `room_area_m2`: `float` ($5.0 \le A \le 200.0$, default: $20.0$)
  - `ceiling_height_m`: `float` ($2.0 \le h \le 5.0$, default: $2.8$)
  - `initial_pm25_ug_m3`: `float` ($5.0 \le C_0 \le 1000.0$, default: $67.7$)
  - `cadr_m3_h`: `float` ($0.0 \le \text{CADR} \le 1200.0$, default: $300.0$; CADR=0 supported)
  - `runtime_hours`: `float` ($0.0 \le t \le 12.0$, default: $2.0$; t=0 supported)
- **Response Schema (`PurificationSimulationResponse`):**
  - `room_volume_m3`: `float` ($A \times h$)
  - `initial_pm25_ug_m3`: `float`
  - `initial_pm25_source`: `"Initialized from outdoor city composite observation (2024-10-31) in the absence of indoor sensors. User-adjustable."`
  - `cadr_m3_h`: `float`
  - `runtime_hours`: `float`
  - `final_pm25_ug_m3`: `float` ($C_0 \times \exp(-\frac{\text{CADR}}{V} \times t)$)
  - `percentage_reduction`: `float`
  - `decay_curve`: Array of **40 evenly spaced interval points** $[(t_i, C_i)]$ ensuring smooth exponential rendering in Recharts without cliff-drop distortion.
  - `formula_used`: `"C(t) = C0 * exp(-(CADR / V) * t)"`
  - `assumptions_ledger`: List of 5 ideal conditions.
  - `disclaimer`: *"Theoretical first-order mass-balance scenario. Not an indoor sensor reading, not an AI prediction, and not a measured purifier test."*

---

## 6. Success Criteria & Verification Gates

- [ ] **Data Zero-Change:** Hashes of all raw files in `data/raw/` identical before and after.
- [ ] **Unit Consistency:** Particulate metrics in $\mu\text{g/m}^3$, CO in $\text{mg/m}^3$, temperature in °C, humidity in %, pressure in hPa, wind in km/h.
- [ ] **Averaging Period Rigor:** Daily CO/$\text{O}_3$ excluded from station AQI; hourly 8h rolling evaluation verified against project 6-of-8 rule.
- [ ] **Lead (Pb) Transparency:** Displays `"Not available in supplied dataset"`, never zero or imputed.
- [ ] **Cluster Stability Gate:** Clustering evaluated with silhouette score and minimum cluster size constraints; fallback to quantile grouping tested.
- [ ] **Physics Simulator Rigor:** Validated for zero runtime, zero CADR, boundary bounds, and monotonic decay.
- [ ] **Automated Test Suite:** All 60 existing tests remain 100% passing; at least 25 new tests added covering new endpoints, schemas, and physics calculations.
- [ ] **100% Offline Integrity:** All new endpoints and frontend views execute with zero external cloud or network requests.
