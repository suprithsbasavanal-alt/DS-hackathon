# System Architecture Specification
# Project BreatheWise — Bengaluru Air Quality & Meteorological Intelligence Platform

**Document Version:** 1.2.0 (Pre-Implementation Gate Finalization)  
**Status:** DRAFT FOR FINAL APPROVAL  
**Execution Standard:** 100% Offline-First  

---

## 1. System Overview & Topological Flow

```
+-----------------------------------------------------------------------------------+
|                        OFFLINE DATA LAKE (data/raw/)                              |
|  - CPCB CAAQM Daily Records: 50,584 records (13 active stations, 1 decommissioned)|
|  - ECMWF ERA5 Reanalysis Weather: 16,080 hourly records (Open-Meteo)              |
|  - Seasonal Hourly CAAQM Slices: 66,947 observations (BTM Layout & Peenya)        |
+-----------------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------------+
|             REPRODUCIBLE DATA PIPELINE (backend/data_pipeline.py)                 |
|  - Temporal Sufficiency Filter: Enforce n >= 16 hours (drops 3,789 records)      |
|  - Deduplication & Timestamp Alignment to Asia/Kolkata (IST, UTC+05:30)           |
|  - Exact CPCB IND-AQI Sub-Index Interpolator (All 8 Criteria Pollutants)        |
|  - Severe Range Numerical Logic: Bounded linear interpolation + 500 ceiling cap   |
|  - CO/O3 Protocol: Excluded from daily AQI (daily mean != 8h); evaluated on hourly|
|  - 24h Criteria Set for Station AQI: PM2.5, PM10, NO2, SO2, NH3 (min 3 rule met)  |
|  - Worst-Pollutant Max Operator (min 3 pollutants, >= 1 particulate matter)      |
|  - City Composite Aggregator: Daily arithmetic mean of reporting station AQIs     |
|  - Chronological Partitioning: Train (2023-01 to 2024-06) / Test (2024-07 to 10)  |
+-----------------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------------+
|                BACKEND API ENGINE (FastAPI on http://127.0.0.1:8000)              |
|  - GET  /api/health                   -> Health, station count, offline status    |
|  - GET  /api/city/summary             -> City composite AQI, category, prominent  |
|  - GET  /api/stations                 -> Station catalog (13 active, 1 decomm.)   |
|  - GET  /api/stations/{id}/summary    -> Latest station AQI, sub-indices, sparkline|
|  - GET  /api/analytics/trends         -> Daily historical time-series             |
|  - GET  /api/analytics/weather-impact -> Retrospective ERA5 correlation matrix    |
|  - GET  /api/analytics/diurnal        -> Validated 24h diurnal profiles (BTM/Peen)|
|  - GET  /api/forecast/backtest        -> Autoregressive predictions vs Persistence|
|  - GET  /api/audit                    -> Completeness metrics, n-hour sufficiency  |
|  - POST /api/scenario/evaluate        -> (Optional) Bounded empirical scenario exp|
+-----------------------------------------------------------------------------------+
                                      |
                                      v  (REST over localhost / Static Mount)
+-----------------------------------------------------------------------------------+
|              FRONTEND DASHBOARD (React + TypeScript + Tailwind CSS)               |
|  - View 1: City Overview (Latest Historical City AQI, 13 Station Cards, Prominent)|
|  - View 2: Deep-Dive Explorer (Daily trends, BTM/Peenya validated diurnal profiles|
|  - View 3: Forecasting Arena (Historical next-day predictions vs Persistence BL)  |
|  - View 4: Health Advisory (CPCB 6-tier health categories, empirical rush advice) |
|  - View 5: Data Transparency (Completeness matrix, n>=16 filter, CPCB formula)   |
|  - (Optional) Scenario Explorer Modal: Bounded empirical scenario testing         |
+-----------------------------------------------------------------------------------+
```

---

## 2. Official CPCB IND-AQI Calculation Methodology

### 2.1 The Official 8-Pollutant Breakpoint Table
Sub-indices and health breakpoints are implemented strictly according to the Central Pollution Control Board (CPCB) 2014 *National Air Quality Index (IND-AQI)* technical report:

| AQI Category | Sub-Index ($I_{LO} - I_{HI}$) | $\text{PM}_{10}$ (24h) $\mu\text{g/m}^3$ | $\text{PM}_{2.5}$ (24h) $\mu\text{g/m}^3$ | $\text{NO}_2$ (24h) $\mu\text{g/m}^3$ | $\text{O}_3$ (8h) $\mu\text{g/m}^3$ | $\text{CO}$ (8h) $\text{mg/m}^3$ | $\text{SO}_2$ (24h) $\mu\text{g/m}^3$ | $\text{NH}_3$ (24h) $\mu\text{g/m}^3$ | $\text{Pb}$ (24h) $\mu\text{g/m}^3$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Good** | $0 - 50$ | $0 - 50$ | $0 - 30$ | $0 - 40$ | $0 - 50$ | $0 - 1.0$ | $0 - 40$ | $0 - 200$ | $0 - 0.5$ |
| **Satisfactory** | $51 - 100$ | $51 - 100$ | $31 - 60$ | $41 - 80$ | $51 - 100$ | $1.1 - 2.0$ | $41 - 80$ | $201 - 400$ | $0.5 - 1.0$ |
| **Moderate** | $101 - 200$ | $101 - 250$ | $61 - 90$ | $81 - 180$ | $101 - 168$ | $2.1 - 10.0$ | $81 - 380$ | $401 - 800$ | $1.1 - 2.0$ |
| **Poor** | $201 - 300$ | $251 - 350$ | $91 - 120$ | $181 - 280$ | $169 - 208$ | $10.1 - 17.0$ | $381 - 800$ | $801 - 1200$ | $2.1 - 3.0$ |
| **Very Poor** | $301 - 400$ | $351 - 430$ | $121 - 250$ | $281 - 400$ | $209 - 748$ | $17.1 - 34.0$ | $801 - 1600$ | $1201 - 1800$ | $3.1 - 3.5$ |
| **Severe** | $401 - 500$ | $> 430$ | $> 250$ | $> 400$ | $> 748$ | $> 34$ | $> 1600$ | $> 1800$ | $> 3.5$ |

### 2.2 Sub-Index Piecewise Linear Formula & Authoritative Severe Range Policy
For an observed concentration $C_p$ of pollutant $p$:
1. If $C_p < 0$, it is invalid (sensor malfunction).
2. For concentrations within categories 1 to 5 (Good to Very Poor, $B_{LO} \le C_p \le B_{HI}$):
   $$I_p = \left[ \frac{I_{HI} - I_{LO}}{B_{HI} - B_{LO}} \right] \times (C_p - B_{LO}) + I_{LO}$$
3. **Project Implementation Policy: Severe Values Reported at the 500 Ceiling:**
   * In the official CPCB 2014 Table 3.2, the Severe category ($401–500$) is open-ended ($C_p > B_{LO, \text{severe}}$) and no upper concentration breakpoint ($B_{HI}$) is published.
   * CPCB published guidelines provide piecewise linear interpolation for categories 1–5, but do not prescribe an official interpolation formula beyond the Severe lower boundary.
   * In BreatheWise, assigning a sub-index of **500.0** when $C_p > B_{LO, \text{severe}}$ is an **explicit project implementation policy** reflecting the CPCB official national index ceiling, NOT an officially prescribed CPCB linear interpolation formula.
   * Separately, raw analyzer readings exceeding the instrument physical measurement range ($>1000\ \mu\text{g/m}^3$) are treated as sensor saturation faults.
   * This policy and all category boundary transitions are verified with 100% pass rate in [`scripts/test_cpcb_calculator.py`](file:///Users/suprith.s.b/Documents/antigravity/DS-hackathon/scripts/test_cpcb_calculator.py).

### 2.3 Regulatory Validity Rules & CO/O3 Averaging Protocol
1. **CO and O3 Exclusion from Daily AQI:**
   * CPCB specifies 8-hour averaging for CO and $\text{O}_3$.
   * Since daily harvested data contains 24-hour daily means, **CO and $\text{O}_3$ sub-indices are strictly excluded from daily station AQI calculations** to avoid substituting daily means for 8-hour values.
   * Station AQI is computed from the 5 valid 24-hour criteria pollutants ($\text{PM}_{2.5}, \text{PM}_{10}, \text{NO}_2, \text{SO}_2, \text{NH}_3$).
   * Genuine 8-hour rolling averages for CO and $\text{O}_3$ are computed and evaluated on the landmark hourly datasets (BTM Layout and Peenya) using a **project-defined completeness threshold of at least 6 of 8 valid hourly observations (75%)**. Windows with $<6$ observations are marked invalid.
2. **16-Hour Sufficiency Rule:** Daily records with $n < 16$ hours are excluded from AQI calculations.
3. **Minimum 3 Pollutants Rule:** Requires at least 3 valid criteria sub-indices with $\text{PM}_{2.5}$ or $\text{PM}_{10}$. All 13 active stations satisfy this rule.
4. **Worst-Pollutant Principle:** Station $\text{AQI} = \max_p(I_p)$. Prominent Pollutant is $\arg\max_p(I_p)$.
5. **City Composite AQI:** Daily arithmetic mean of reporting active stations' valid AQIs.

---

## 3. Retrospective Meteorological Analysis vs Operational Forecasting

### 3.1 Retrospective Historical Correlation Analysis (Screen 2)
- Evaluates surface ventilation and precipitation wet scavenging using ECMWF ERA5 reanalysis surface data (temperature, humidity, precipitation, orthogonal $u, v$ wind vectors, surface pressure).
- Labeled explicitly as **Retrospective Historical Correlation Analysis**, strictly separated from forecasting.
- Surface temperature measurements are not used to claim thermal inversions.

### 3.2 Autoregressive Next-Day Forecasting (Zero Weather Leakage)
- **Strict Information Cutoff at Time $t$:**
  * Forecast target: Next-day particulate concentrations ($\widehat{\text{PM}}_{2.5, t+1}, \widehat{\text{PM}}_{10, t+1}$).
  * Available features at time $t$:
    - Autoregressive lags: $\text{PM2.5}_t, \text{PM2.5}_{t-1}, \text{PM2.5}_{t-2}, \text{PM10}_t, \dots$
    - Past rolling statistics up to day $t$.
    - Realized weather features up to day $t$.
    - Calendar features of day $t+1$.
    - **ZERO realized weather features from target day $t+1$ are leaked to the model.**
- **Chronological Split:**
  * Training: 2023-01-01 to 2024-06-30.
  * Held-Out Test: 2024-07-01 to 2024-10-31.
- **Baselines:** Persistence Baseline ($\text{AQI}_{t+1} = \text{AQI}_t$) and 7-Day Moving Average.
- **Evaluation Persistence:** Realized MAE, RMSE, and $R^2$ dynamically read from `data/processed/model_evaluation.json`.

---

## 4. Historical Station-Specific Diurnal Observations (BTM Layout & Peenya)

From empirical analysis of 66,947 hourly observations across 4 seasonal benchmark months in 2024 at BTM Layout (`site_162`) and Peenya (`site_163`):
1. **$\text{NO}_2$ Profile:** At BTM Layout, $\text{NO}_2$ concentrations are highest in the morning hours between **07:00 and 09:00** ($36.33\ \mu\text{g/m}^3$ at 08:00) and lower during midday (**11:00–13:00**, $29.67 - 30.67\ \mu\text{g/m}^3$).
2. **Particulate Matter ($\text{PM}_{10}$ and $\text{PM}_{2.5}$) and $\text{CO}$ Profiles:** Display observed elevations:
   - Late evening and night (**20:00–23:00**, reaching $71.84\ \mu\text{g/m}^3$ $\text{PM}_{10}$ at BTM, $76.97\ \mu\text{g/m}^3$ at Peenya).
   - Secondary morning peak (**08:00–09:00**, $65.49\ \mu\text{g/m}^3$ $\text{PM}_{10}$ at BTM).
   - Lower midday levels (**12:00–16:00**, $46.78\ \mu\text{g/m}^3$ at BTM).
3. **Data Scope & Integrity Notice:** These curves represent historical descriptive observations recorded specifically at BTM Layout and Peenya. They are not extrapolated as city-wide generalizations, and unevidenced causal claims (such as convective dilution or nocturnal cooling mechanisms) are intentionally omitted.

### 4.1 8-Hour Rolling Average Protocol for CO and Ozone
- **Sufficiency Rule:** While CPCB specifies 8-hour averaging for CO and $\text{O}_3$, the requirement of at least 75% completeness (minimum 6 valid hourly observations within the 8-hour window) is an explicit **project-defined completeness threshold** (not a CPCB-prescribed formula). Windows with $<6$ valid observations are discarded as invalid.
- **Audit Findings ([`audit_8hour_rolling_report.json`](file:///Users/suprith.s.b/Documents/antigravity/DS-hackathon/data/processed/audit_8hour_rolling_report.json)):**
  * BTM Layout: 2,848 valid CO 8h windows (98.6% validity rate); 2,841 valid Ozone 8h windows (98.3% validity rate).
  * Peenya: 2,594 valid CO 8h windows (88.7% validity rate); 2,394 valid Ozone 8h windows (81.8% validity rate).
  * Total valid rolling 8-hour evaluation windows: **10,677 valid windows** out of 11,632 possible slots (**91.8% overall validity rate**).

---

## 5. Detailed API Specification

| Method | Endpoint | Query / Body Parameters | Response Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | None | Service status, offline mode flag, total records |
| `GET` | `/api/city/summary` | None | Latest historical city composite AQI, category, prominent pollutant, active station count, date |
| `GET` | `/api/stations` | None | Catalog of all 14 stations with coordinates, parameters, and `is_active` flag (13 active, 1 decomm.) |
| `GET` | `/api/stations/{id}/summary` | None | Station latest AQI, 5 valid 24h sub-indices, prominent pollutant, 30-day sparkline |
| `GET` | `/api/analytics/trends` | `station_id`, `start_date`, `end_date` | Filtered daily historical time-series of criteria pollutants and calculated AQI |
| `GET` | `/api/analytics/weather-impact` | None | Retrospective correlation matrix between ERA5 weather variables and pollutant levels |
| `GET` | `/api/analytics/diurnal` | `station_id` (site_162 or site_163), `month` | Empirically validated 24h hourly profiles for landmark stations |
| `GET` | `/api/forecast/backtest` | `station_id` | Autoregressive next-day predictions vs Persistence baseline on held-out test window |
| `GET` | `/api/audit` | None | Complete data completeness report, missing station-days, $n \ge 16$ sufficiency counts |
| `POST`| `/api/scenario/evaluate` | `{station_id?: str, temp_delta: float, wind_delta: float, rain_delta: float}` | (Optional / Experimental) Bounded empirical scenario explorer with input domain checks |
