# BreatheWise Complete AI Expansion — Comprehensive Implementation Plan & Technical Contracts

> **Author**: Antigravity Full-Stack Data Science Agent  
> **Status**: PLANNING ONLY (Code Freeze in Effect until Explicit User Approval)  
> **References**: `.gsd/SPEC.md`, `.gsd/ROADMAP.md`, `PROJECT_RULES.md`, `rules.md`

---

## 1. Data, Averaging-Period & Threshold Matrix

This matrix establishes the scientific and regulatory protocol for all criteria pollutants and meteorological variables present in the dataset.

| Variable | Raw Source & Key | Unit | Supported Averaging Period | CPCB Table 3.2 Breakpoints / Tiers | Daily Station AQI Inclusion | Benchmark Scope / Notes |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- |
| **$\text{PM}_{2.5}$** | `bengaluru_daily_combined_raw.json` (`PM2.5`) | $\mu\text{g/m}^3$ | 24-hour arithmetic mean | Good: 0–30, Satisfactory: 31–60, Moderate: 61–90, Poor: 91–120, Very Poor: 121–250, Severe: $>250$ (500 ceiling policy) | **Yes** (Requires $\ge 16$h) | Monitored across all 13 active stations (2023–2024). Mandatory particulate requirement for valid AQI. |
| **$\text{PM}_{10}$** | `bengaluru_daily_combined_raw.json` (`PM10`) | $\mu\text{g/m}^3$ | 24-hour arithmetic mean | Good: 0–50, Satisfactory: 51–100, Moderate: 101–250, Poor: 251–350, Very Poor: 351–430, Severe: $>430$ (500 ceiling policy) | **Yes** (Requires $\ge 16$h) | Monitored across all 13 active stations. Primary driver of Bengaluru Moderate AQI. |
| **$\text{NO}_2$** | `bengaluru_daily_combined_raw.json` (`NO2`) | $\mu\text{g/m}^3$ | 24-hour arithmetic mean | Good: 0–40, Satisfactory: 41–80, Moderate: 81–180, Poor: 181–280, Very Poor: 281–400, Severe: $>400$ (500 ceiling policy) | **Yes** (Requires $\ge 16$h) | Vehicular emissions tracer; exhibits pronounced morning peak (07:00–09:00). |
| **$\text{SO}_2$** | `bengaluru_daily_combined_raw.json` (`SO2`) | $\mu\text{g/m}^3$ | 24-hour arithmetic mean | Good: 0–40, Satisfactory: 41–80, Moderate: 81–380, Poor: 381–800, Very Poor: 801–1600, Severe: $>1600$ (500 ceiling policy) | **Yes** (Requires $\ge 16$h) | Consistently low baseline ($< 15\ \mu\text{g/m}^3$) across Bengaluru throughout 2023–2024. |
| **$\text{NH}_3$** | `bengaluru_daily_combined_raw.json` (`NH3`) | $\mu\text{g/m}^3$ | 24-hour arithmetic mean | Good: 0–200, Satisfactory: 201–400, Moderate: 401–800, Poor: 801–1200, Very Poor: 1201–1800, Severe: $>1800$ (500 ceiling policy) | **Yes** (Requires $\ge 16$h) | Agriculture/waste tracer; values in Bengaluru remain well within Good tier ($< 30\ \mu\text{g/m}^3$). |
| **$\text{CO}$** | `bengaluru_daily_combined_raw.json` (`CO`) | $\text{mg/m}^3$ | **8-hour rolling average only** | Good: 0–1.0, Satisfactory: 1.1–2.0, Moderate: 2.1–10.0, Poor: 10.1–17.0, Very Poor: 17.1–34.0, Severe: $>34.0$ (500 ceiling policy) | **NO** (Strictly excluded from 24h daily AQI) | Daily archive records are 24-hour means. Evaluated only on BTM/Peenya hourly slices with project $\ge 6$ of 8h (75%) rule. |
| **$\text{O}_3$ (Ozone)** | `bengaluru_daily_combined_raw.json` (`Ozone`) | $\mu\text{g/m}^3$ | **8-hour rolling average only** | Good: 0–50, Satisfactory: 51–100, Moderate: 101–168, Poor: 169–208, Very Poor: 209–748, Severe: $>748$ (500 ceiling policy) | **NO** (Strictly excluded from 24h daily AQI) | Daily archive records are 24-hour means. Evaluated only on BTM/Peenya hourly slices with project $\ge 6$ of 8h (75%) rule. |
| **$\text{Pb}$ (Lead)** | *None* | $\mu\text{g/m}^3$ | 24-hour arithmetic mean | Good: 0–0.5, Satisfactory: 0.5–1.0, Moderate: 1.1–2.0, Poor: 2.1–3.0, Very Poor: 3.1–3.5, Severe: $>3.5$ | **NO** (Missing) | **Unavailable in supplied dataset.** Never fabricated or imputed. Explicitly displayed as `"Not available in supplied dataset"`. |
| **Temperature** | `bengaluru_weather_openmeteo.json` | °C | Hourly & 24h mean/min/max | **Zero regulatory CPCB thresholds.** Descriptive percentiles: P10: 20.1°C, P50: 24.3°C, P90: 28.5°C | N/A | ERA5 atmospheric reanalysis at surface level ($2\text{m}$). |
| **Relative Humidity** | `bengaluru_weather_openmeteo.json` | % | Hourly & 24h mean | **Zero regulatory CPCB thresholds.** Descriptive percentiles: Dry: $<60\%$, Moderate: $60–80\%$, Humid: $>80\%$ | N/A | Strong seasonal variance between monsoon ($>80\%$) and post-monsoon dry months. |
| **Precipitation** | `bengaluru_weather_openmeteo.json` | $\text{mm}$ | Daily accumulation sum | **Zero regulatory CPCB thresholds.** Descriptive categories: Trace: $<1\text{mm}$, Light: $1–10\text{mm}$, Heavy: $>10\text{mm}$ | N/A | Wet particulate scavenging correlates negatively with $\text{PM}_{10}$ ($r = -0.431$). |
| **Resultant Wind Speed** | `bengaluru_weather_openmeteo.json` | $\text{km/h}$ | Vector-averaged resultant speed | **Zero regulatory CPCB thresholds.** Descriptive bands: Stagnant: $<5\text{km/h}$, Moderate: $5–15\text{km/h}$, Breezy: $>15\text{km/h}$ | N/A | Decomposed into orthogonal vectors ($u, v$); aerodynamic dispersion correlates negatively with $\text{PM}_{2.5}$ ($r = -0.263$). |
| **Resultant Wind Direction** | `bengaluru_weather_openmeteo.json` | Degrees (°) | Vector-averaged azimuth ($0–360^\circ$) | **Zero regulatory CPCB thresholds.** Descriptive compass quadrants: N, NE, E, SE, S, SW, W, NW | N/A | Reconstructed via $\text{atan2}(-\bar{u}, -\bar{v})$. Never averaged arithmetically. |
| **Surface Pressure** | `bengaluru_weather_openmeteo.json` | $\text{hPa}$ | Hourly & 24h mean | **Zero regulatory CPCB thresholds.** Descriptive percentiles: Low: $<910\text{hPa}$, Typical: $910–915\text{hPa}$, High: $>915\text{hPa}$ | N/A | Higher surface pressure was historically associated with higher city AQI in this dataset ($r = +0.607$). |

---

## 2. Machine Learning Model Cards

### Model Card 1: Unsupervised Exploratory Environmental Regimes
- **Component ID:** `ML-REGIME-01`
- **Model Type:** Unsupervised Standardized $k$-Means Clustering with Heuristic Gating & Automated Quantile Fallback.
- **Intended Purpose:** Discover exploratory multi-pollutant and atmospheric regime groupings across Bengaluru's historical daily record (Jan 1, 2023 to Oct 31, 2024).
- **Target Variable:** None (Unsupervised clustering).
- **Input Features ($d=8$ Standardized Features):**
  1. `pm25` (standardized)
  2. `pm10` (standardized)
  3. `no2` (standardized)
  4. `temp_mean` (standardized)
  5. `humidity_mean` (standardized)
  6. `wind_u` (zonal vector component, standardized)
  7. `wind_v` (meridional vector component, standardized)
  8. `pressure_mean` (standardized)
  - *Scalar Wind Speed Exclusion Rationale:* In meteorology, $\text{WindSpeed} = \sqrt{u^2 + v^2}$. Including scalar speed alongside orthogonal components $u$ and $v$ double-weights kinetic wind magnitude in Euclidean distance calculations. Scalar speed is therefore excluded from clustering distances, retaining clean orthogonal vector components.
- **Empirical Completeness Verification:**
  - Audited across all 670 daily city composite records in `data/processed/city_daily_summary.json`.
  - **Result: 0 missing values (100.00% complete) across all 8 features.**
  - Predictor completeness is verified directly from data, not inferred from city AQI.
  - **Station-Level Fallback:** For individual station queries where missing days exist, missingness is dynamically reported with exact $N_{\text{valid}}$ and coverage percentages; clustering is precomputed and served from the complete city composite matrix.
- **Model Selection & Heuristic Stability Gate:**
  - Evaluates $k \in \{2, 3, 4, 5\}$ using `scikit-learn`'s `KMeans(random_state=42, n_init=10)`.
  - Computes Mean Silhouette Score $S(k)$, cluster inertia, and cluster size distribution.
  - **Empirical Results on 670 Days ($d=8$):**
    - $k=2$: Silhouette = $0.3497$, Inertia = $3323.5$, Counts = [351, 319]
    - $k=3$: Silhouette = **$0.3557$** (Optimal peak), Inertia = **$2601.0$**, Counts = [338, 130, 202] (Min cluster: 19.40%, 130/670)
    - $k=4$: Silhouette = $0.2425$, Inertia = $2290.8$, Counts = [129, 159, 186, 196]
    - $k=5$: Silhouette = $0.2445$, Inertia = $2040.8$, Counts = [193, 63, 123, 150, 141]
  - **Multi-Seed Stability Verification (Seeds 42, 100, 2024, 7, 99):**
    - Pairwise Adjusted Rand Index (ARI) = **$1.0000$ across all 10 seed pairs**.
    - Cluster size distribution is perfectly invariant across seeds: $\{338, 202, 130\}$.
  - **Heuristic Acceptance Criterion:** The silhouette threshold ($S \ge 0.30$) is an **analytical project acceptance heuristic**, not scientific proof of physical cluster structure.
  - If $S < 0.30$ OR any cluster contains $< 5\%$ of samples ($< 33$ days), cluster labeling is disabled: sets `is_fallback: true` and falls back to deterministic seasonal quantile groupings.
- **Precomputed Caching:**
  - Serialized as `data/processed/environmental_regimes.json` for zero-latency, sub-millisecond offline delivery.
- **Ethical & Scientific Disclosures:**
  - **Non-Causal Notice:** Clusters represent empirical co-occurrence patterns, NOT pollution source attribution or atmospheric causation.
  - **Zero Overfitting Claim:** No generalization to unmonitored future years is claimed.

---

### Model Card 2: Next-Day Autoregressive Forecasting Benchmark (Existing Preserved)
- **Component ID:** `ML-FORECAST-01`
- **Model Type:** Random Forest Regressor vs. Naive Persistence Baseline ($\text{AQI}_{t+1} = \text{AQI}_t$) vs. Two-Stage Physical Concentration Model vs. 7-Day Moving Average.
- **Intended Purpose:** Transparent benchmark evaluation of 24-hour next-day AQI prediction.
- **Target Variable:** $\text{City AQI}_{t+1}$ (Direct RF) and $[\text{PM}_{2.5, t+1}, \text{PM}_{10, t+1}]$ (Two-Stage Physical Model).
- **Sample Size:** 670 calendar days (Jan 1, 2023 to Oct 31, 2024).
- **Validation Split:** Chronological held-out test split:
  - Training Set: Jan 8, 2023 to Jun 30, 2024 ($N = 546$ days, matching `model_evaluation.json`)
  - Held-out Test Set: Jul 1, 2024 to Oct 31, 2024 ($N = 123$ days)
  - Zero cross-validation shuffling across time. Zero target-day weather leakage.
- **Evaluation Metrics (Held-out 123 Days):**
  - **Persistence Baseline:** MAE = 7.42 points, RMSE = 10.49, $R^2 = 0.733$ (**Primary Benchmark**)
  - **Direct AQI Random Forest:** MAE = 7.74 points, RMSE = 11.14, $R^2 = 0.699$
  - **Two-Stage Physical Model:** MAE = 7.91 points, RMSE = 12.43, $R^2 = 0.625$
  - **7-Day Moving Average:** MAE = 9.20 points, RMSE = 15.08, $R^2 = 0.449$
- **Core Finding & Disclosure:**
  - *"Our evaluation showed that the simple persistence baseline outperformed both machine-learning approaches on the held-out test period. This demonstrates why complex models must be tested against simple baselines before claiming predictive value."*

---

### Physics Model Card: Theoretical Air Purification Simulator
- **Component ID:** `PHYS-PURIFIER-01`
- **Model Type:** Idealized first-order mass-balance exponential decay equation. **NOT an AI model.**
- **Mathematical Formulation:**
  $$V = A \times h \quad (\text{m}^3)$$
  $$C(t) = C_0 \times \exp\left(-\frac{\text{CADR}}{V} \times t\right) \quad (\mu\text{g/m}^3)$$
  $$\text{Reduction} = \left(1 - \frac{C(t)}{C_0}\right) \times 100\%$$
- **Validated Parameter Ranges:**
  - Floor Area $A \in [5.0, 200.0]\ \text{m}^2$
  - Ceiling Height $h \in [2.0, 5.0]\ \text{m}$
  - Starting $\text{PM}_{2.5}$ $C_0 \in [5.0, 1000.0]\ \mu\text{g/m}^3$ (Source metadata: *"Initialized from outdoor city composite observation (2024-10-31) in the absence of indoor sensors. User-adjustable."*)
  - CADR $\in [0.0, 1200.0]\ \text{m}^3/\text{h}$ (Default: $300.0$; CADR=0 supported for pre-operation baseline)
  - Duration $t \in [0.0, 12.0]\ \text{hours}$ (Default: $2.0$; t=0 supported for initial state)
- **Curve Sampling:** 40 evenly spaced points along $[0, t]$ to prevent Recharts cliff-drop distortion.
- **Boundary Proofs:**
  - $t = 0 \implies C(t) = C_0, \text{Reduction} = 0.0\%$
  - $\text{CADR} = 0 \implies C(t) = C_0, \text{Reduction} = 0.0\%$
  - $\forall t_2 > t_1 \ge 0, C(t_2) < C(t_1)$ (Strict monotonic decay when $\text{CADR} > 0$)
  - $0 \le C(t) \le C_0$ for all valid inputs.
- **Explicit Assumptions Ledger:**
  1. Instantaneous and perfect spatial mixing (no dead zones or localized concentration gradients).
  2. Zero continuing indoor emission sources (no cooking, smoking, incense, or dust resuspension).
  3. Zero infiltration of outdoor pollutants through doors, windows, and building envelope cracks.
  4. Zero natural particle deposition, gravitational settling, or wall loss.
  5. Continuous purifier operation at rated CADR without filter degradation, bypass, or airflow reduction.
- **Mandatory Disclaimers:**
  - *"This is a simplified theoretical scenario, not a real-world guarantee, not an indoor sensor reading, not a purifier test and not an AI prediction."*

---

## 3. File-by-File Implementation Plan

### Backend Modules to Implement
1. **`backend/schemas/environmental.py` (New)**: Pydantic v2 models for `EnvironmentalInsightsResponse`, `PollutantStatusItem`, `MeteorologyContextItem`, and `CorrelationItem`.
2. **`backend/schemas/regimes.py` (New)**: Pydantic v2 models for `EnvironmentalRegimesResponse`, `RegimeProfileItem`, and `DiagnosticMetrics`.
3. **`backend/schemas/health.py` (New)**: Pydantic v2 models for `HealthAdvisoryResponse`, `TriggeredAdvisoryItem`, and `SensitiveGroupAdvice`.
4. **`backend/schemas/purification.py` (New)**: Pydantic v2 models for `PurificationSimulationRequest` and `PurificationSimulationResponse`.
5. **`backend/threshold_engine.py` (New)**: Pure adapter calling `cpcb_calculator.py`. Handles unit validations, CPCB Table 3.2 tier mappings, Pb absence handling, and CO/$\text{O}_3$ averaging checks.
6. **`backend/environmental_analysis.py` (New)**: Computes unified multi-pollutant summaries and Pearson/Spearman correlation matrices with sample counts from `data/processed/city_daily_summary.json`.
7. **`backend/environmental_regimes.py` (New)**: Standardizes features, computes $k$-Means ($k \in [2, 5]$), calculates silhouette scores, validates minimum cluster sizes, and outputs regime profiles or deterministic seasonal fallback.
8. **`backend/health_advisor.py` (New)**: Deterministic rule engine evaluating CPCB AQI tiers and pollutant thresholds with authoritative rule catalog:
   - `RULE-AQI-GOOD-01` (0–50): Minimal impact; outdoor activities encouraged.
   - `RULE-AQI-SAT-01` (51–100): Minor breathing discomfort to sensitive people.
   - `RULE-AQI-MOD-01` (101–200): Breathing discomfort to people with asthma and heart disease.
   - `RULE-AQI-POOR-01` (201–300): Breathing discomfort to most people on prolonged exposure.
   - `RULE-AQI-VPOOR-01` (301–400): Respiratory illness on prolonged exposure.
   - `RULE-AQI-SEV-01` (401–500): Severe health impact even on healthy people; physical exertion avoided.
   - `RULE-PM25-ELEV-01` ($\text{PM}_{2.5} > 60\ \mu\text{g/m}^3$): Particulate alert for sensitive cohorts.
   - `RULE-PM10-ELEV-01` ($\text{PM}_{10} > 100\ \mu\text{g/m}^3$): Coarse dust transit alert.
   - `RULE-NO2-RUSH-01` ($\text{NO}_2 > 40\ \mu\text{g/m}^3$): Rush-hour vehicular exposure guidance.
9. **`backend/purification_simulator.py` (New)**: Validates input boundaries (allowing CADR=0, t=0) and executes the idealized well-mixed first-order decay equation, generating a 40-point decay curve.
10. **`backend/main.py` (Update)**: Mounts the 4 new endpoints without modifying existing 9 endpoints. `GET /api/ai/regimes` serves precomputed static JSON.
11. **Unit & Integration Tests (New)**:
    - `backend/test_environmental.py`: Tests threshold mapping, Pb missingness, unit checks, 24h CO/O3 null sub-indices, and correlation sample counts.
    - `backend/test_regimes.py`: Tests cluster stability gate, silhouette thresholds, and fallback behavior.
    - `backend/test_health_advisor.py`: Tests rule triggers, evidence formatting, and disclaimers.
    - `backend/test_purification.py`: Tests boundary conditions, CADR=0, t=0, monotonic decay, and input validation errors.

### Frontend Components to Implement
1. **`frontend/src/types/index.ts` (Update)**: Adds TypeScript interfaces for all new API schemas.
2. **`frontend/src/services/api.ts` (Update)**: Adds typed fetchers: `fetchAIInsights()`, `fetchRegimes()`, `fetchHealthAdvisories()`, `simulatePurification()`.
3. **`frontend/src/components/PurificationSimulator.tsx` (New)**: Interactive simulator panel with area/height/CADR/time sliders, dynamic room volume, Recharts exponential decay curve (40 points), formula callout (rendered using clean semantic HTML without heavy math libraries), and assumption disclosures.
4. **`frontend/src/views/AIInsightsView.tsx` (New)**: Full dashboard view featuring:
   - Historical date warning banner.
   - Environmental snapshot cards.
   - 7 criteria pollutants + Pb threshold assessment table (with CO/O3 8h standard notice and Pb unavailable label).
   - Retrospective weather correlation matrix with sample counts.
   - Environmental regime profiles or diagnostic fallback alert.
   - Deterministic health advisory cards with rule IDs and triggers.
   - Embedded purification recommendation and simulator launcher.
5. **`frontend/src/App.tsx` (Update)**: Adds `#ai-insights` tab to top navigation bar with responsive styling to prevent layout wrapping on 768px–1024px tablet viewports.

---

## 4. Adversarial EGM/Goldfish Review Checklist

| Check Area | Verification Requirement | Pass/Fail Gate |
| :--- | :--- | :---: |
| **Leakage Guard** | Are target-day ($t+1$) weather parameters withheld from all forecasting features? | **MANDATORY PASS** |
| **Persistence Truth** | Does every presentation of forecasting clearly show Persistence (7.42) outperforming ML (7.74 / 7.91)? | **MANDATORY PASS** |
| **Averaging Period Rigor** | Are daily 24h CO and $\text{O}_3$ strictly excluded from daily station AQIs? Are 8h rolling metrics restricted to BTM/Peenya? | **MANDATORY PASS** |
| **Lead (Pb) Transparency** | Is Pb explicitly labeled as `"Not available in supplied dataset"`, with zero imputation or fake zeroes? | **MANDATORY PASS** |
| **Threshold Misuse** | Are meteorological variables strictly evaluated with descriptive percentiles, with zero CPCB regulatory claims? | **MANDATORY PASS** |
| **Causality Enforcement** | Are all correlations, regressions, and feature importances framed strictly as retrospective associations? | **MANDATORY PASS** |
| **Cluster Stability Gate** | Is the unsupervised clustering protected by an analytical acceptance heuristic ($S \ge 0.30$) and an automated deterministic seasonal fallback? | **MANDATORY PASS** |
| **Purifier Demarcation** | Is the purification simulator explicitly formulated as a theoretical physics formula and NOT an AI model or sensor measurement? | **MANDATORY PASS** |
| **Health Advice Scope** | Are health recommendations deterministic, mapped to rule IDs and CPCB tiers, with clear non-medical disclaimers? | **MANDATORY PASS** |
| **100% Offline-First** | Do all new modules, endpoints, and frontend components execute locally with zero internet access? | **MANDATORY PASS** |

---

## 5. Risk Register & Unresolved Questions

### Risk Register
1. **Risk 1: Cluster Instability on 670 Daily Observations**  
   *Likelihood:* Medium | *Impact:* Medium  
   *Mitigation:* Implement automated silhouette evaluation ($S \ge 0.30$) and minimum cluster size checks ($>5\%$). If clustering is noisy or unstable, automatically disable cluster labels and fall back to transparent seasonal quantile groupings.
2. **Risk 2: Misinterpretation of the Purification Simulator**  
   *Likelihood:* High | *Impact:* High  
   *Mitigation:* Prominently label the panel as *"Hypothetical Physics Calculation • User-Entered Assumptions • Not an AI Model • Not an Indoor Sensor Reading"*. Display the exact mathematical formula ($C(t) = C_0 e^{-\frac{\text{CADR}}{V}t}$) and the 5 ideal assumptions directly on the UI.
3. **Risk 3: Frontend Bundle Size Expansion**  
   *Likelihood:* Low | *Impact:* Low  
   *Mitigation:* Reuse existing `recharts`, `lucide-react`, and Tailwind CSS tokens without adding heavy new UI or chart libraries.
4. **Risk 4: Upstream Starlette Deprecation Warning**  
   *Likelihood:* High | *Impact:* Low  
   *Mitigation:* Maintain the warning in the test documentation as an active test-client dependency notice without claiming "zero impact" as an absolute proof.

### Explicit Unresolved Questions for User Alignment
1. **Placement of the Purification Simulator:** We have designed the Purification Simulator as a reusable component embedded within `AIInsightsView.tsx`, while also adding a quick-launcher modal/tab in `HealthAdvisoryView.tsx`. Does this dual entry point match your expectations, or do you prefer it exclusively inside `AIInsightsView.tsx`?
2. **Cluster Count Granularity:** We propose evaluating $k \in [2, 5]$ with optimal $k$ selected via silhouette score (defaulting to 3 if stability passes: e.g., Dry Stagnant, Monsoon Cleansing, Convective Transitional). Does this 3-regime resolution align with your analytical goals?
