# Project Memory & Decision Log

## 1. Project Context & Foundation
- **Project Name:** BreatheWise
- **Challenge Domain:** Urban Environmental Intelligence (Air Quality & Weather Dynamics)
- **City & Region:** Bengaluru, Karnataka, India
- **Core Directive:** 8-hour autonomous development operating system for Data Science Hackathon.
- **Operating Standards:**
  - Autonomy: Autonomous execution, stopping only at planning sign-off, critical ambiguity, or destructive steps.
  - Priority: Working product > Genuine data > Actionable insight > Premium UI > Documentation.
  - Verification: Zero synthetic/fake data; offline-first local execution.
  - Communication: Tailored for 2nd-year CSE Data Science student (clear data/model rationale, precise commands).

## 2. Problem Statement & Objectives
- **Core Challenge:** Build an offline-first Data Science platform that combines ground-truth CPCB continuous ambient air quality monitoring (CAAQM) with ECMWF ERA5 reanalysis weather data to compute official IND-AQI, expose spatial disparities across Bengaluru, analyze diurnal and seasonal trends, evaluate historical next-day forecasts without target weather leakage, and provide CPCB-grounded health advisories.

## 3. Verified Data Sources & Provenance
- **Air Quality Source:** Central Pollution Control Board (CPCB) continuous monitoring network via XKDR Forum CAAQM API (`https://airquality.xkdr.org/`).
- **Meteorological Source:** ECMWF ERA5 Atmospheric Reanalysis via Open-Meteo Historical Weather API (`https://open-meteo.com/`). Grid centered on 12.97°N, 77.56°E, elevation 910.0m.
- **Station Network (14 Cataloged Stations):**
  * 13 Active Reporting Stations across 2023–2024:
    - Central: City Railway Station (`site_165`)
    - South: BTM Layout (`site_162`), Silk Board (`site_1558`), Jayanagar 5th Block (`site_1556`), Hombegowda Nagar (`site_1555`)
    - North: Hebbal (`site_1554`), Kasturi Nagar (`site_5681`)
    - West: Peenya Industrial (`site_163`), Shivapura Peenya (`site_5686`), Bapuji Nagar (`site_1553`), Saneguruvanahalli (`site_166`), RVCE-Mailasandra (`site_5678`)
    - Far South: Jigani (`site_5729`)
  * 1 Decommissioned Station: BWSSB Kadabesanahalli (`site_164`, closed Aug 2022; 0 records in 2023–2024, preserved in catalog with `is_active: false`).

## 4. Rigorous Pre-Implementation Gate Resolutions

### Blocker 1: Project Implementation Policy: Severe Values Reported at the 500 Ceiling
- **CPCB Regulatory Standard (CPCB 2014 Table 3.2):**
  * Table 3.2 defines open-ended concentration ranges for the Severe category ($C_p > B_{LO, \text{severe}}$: $\text{PM}_{10} > 430, \text{PM}_{2.5} > 250, \text{NO}_2 > 400, \text{SO}_2 > 1600, \text{NH}_3 > 1800, \text{Pb} > 3.5, \text{CO} > 34, \text{O}_3 > 748$).
  * CPCB publishes **no upper concentration breakpoints** for the Severe category.
  * CPCB guidelines provide piecewise linear interpolation for categories 1–5, but do not prescribe an official interpolation formula beyond the Severe lower boundary.
  * In BreatheWise, assigning a sub-index of **500.0** when $C_p > B_{LO, \text{severe}}$ is an **explicit project implementation policy** reflecting the CPCB official national index ceiling, NOT an officially prescribed CPCB linear interpolation formula.
  * Separately, raw analyzer readings exceeding the physical measurement range of standard CAAQM analyzers ($>1000\ \mu\text{g/m}^3$) are treated as sensor saturation faults.
  * Zero arbitrary upper concentration breakpoints are invented.
- **Unit Test Verification ([`scripts/test_cpcb_calculator.py`](file:///Users/suprith.s.b/Documents/antigravity/DS-hackathon/scripts/test_cpcb_calculator.py)):**
  * Executed with 100% pass rate:
    - At exact Severe lower threshold ($C = 250.0$ for $\text{PM}_{2.5}$): Sub-index = $400.0$ (Very Poor).
    - Immediately above threshold ($C = 250.1$ for $\text{PM}_{2.5}$): Sub-index = $500.0$ (Severe).
    - Extreme saturation spikes ($C = 893.0$ for $\text{PM}_{2.5}$): Sub-index = $500.0$ (Severe).
    - At exact threshold ($C = 430.0$ for $\text{PM}_{10}$): Sub-index = $400.0$ (Very Poor).
    - Immediately above threshold ($C = 431.0$ for $\text{PM}_{10}$): Sub-index = $500.0$ (Severe).
    - Extreme spikes ($C = 650.0$ for $\text{PM}_{10}$): Sub-index = $500.0$ (Severe).
    - Negative concentrations rejected (None).
    - Minimum 3 pollutants rule strictly enforced.

### Blocker 2: CO and O3 Averaging Protocol & 8-Hour Rolling Window Audit
- CPCB specifies 8-hour averaging for CO and $\text{O}_3$.
- Because daily harvested records represent 24-hour daily means, **CO and $\text{O}_3$ sub-indices are strictly excluded from daily station AQI calculations** to prevent substituting 24-hour means for 8-hour metrics.
- Station AQI is calculated using the 5 valid 24-hour criteria pollutants ($\text{PM}_{2.5}, \text{PM}_{10}, \text{NO}_2, \text{SO}_2, \text{NH}_3$).
- **8-Hour Rolling Window Audit ([`audit_8hour_rolling_report.json`](file:///Users/suprith.s.b/Documents/antigravity/DS-hackathon/data/processed/audit_8hour_rolling_report.json)):**
  * Enforced a **project-defined completeness threshold of at least 6 of 8 valid hourly observations (75%)**. Windows with $<6$ observations are marked invalid.
  * 10,677 valid 8-hour rolling windows out of 11,632 possible windows (**91.8% overall validity rate** across BTM Layout and Peenya).

### Blocker 3: Forecasting Data Leakage Elimination
- Target-day ($t+1$) realized ERA5 weather is **strictly withheld** from the operational forecasting model.
- At forecast issue time $t$, the model uses **ONLY information available at time $t$**:
  * Autoregressive pollutant lags ($\text{PM2.5}_t, \text{PM2.5}_{t-1}, \dots$)
  * Past rolling statistics up to day $t$
  * Realized weather up to day $t$
  * Calendar indicators of day $t+1$
- Retrospective weather-pollution correlation analysis (Screen 2) is maintained as an explicitly labeled historical analysis module.

### Additional Requirement Resolutions
1. **Station-Specific Diurnal Observations:** Descriptive findings from 66,947 observations at BTM Layout and Peenya (`scripts/validate_rush_hour.py`):
   - At BTM Layout, $\text{NO}_2$ averages are highest in the morning (07:00–09:00, $36.33\ \mu\text{g/m}^3$) and lower during midday ($29.67 - 30.67\ \mu\text{g/m}^3$).
   - At both stations, $\text{PM}_{10}$ and $\text{PM}_{2.5}$ averages in the dataset are higher in the late evening (20:00–22:00, $71.84\ \mu\text{g/m}^3$ at BTM, $76.97\ \mu\text{g/m}^3$ at Peenya) than during midday (12:00–16:00, $46.78\ \mu\text{g/m}^3$ at BTM), with a secondary morning peak (08:00–09:00, $65.49\ \mu\text{g/m}^3$).
   - Labeled strictly as historical station-specific patterns without unevidenced causal claims.
2. **Health Advisory:** Grounded in official CPCB 6-tier categories; diurnal timing patterns presented as historical station-specific observations rather than universal medical advice.
3. **What-If Simulator:** Moved to Optional / Experimental status, outside the critical MVP path.

## 5. Implementation Verification Ledger (Phase 4 Completed)

- **Approval Received:** User sent `Approve Phase 4 — Start implementation.`
- **Deliverables Completed:**
  1. [`backend/cpcb_calculator.py`](file:///Users/suprith.s.b/Documents/antigravity/DS-hackathon/backend/cpcb_calculator.py):
     - Official CPCB Table 3.2 IND-AQI calculation for categories 1–5.
     - Project implementation policy reporting Severe values at the 500 ceiling cap.
     - CO and O3 excluded from daily 24h station AQI.
     - Minimum 3 criteria pollutants and particulate matter requirements.
     - Verified by 43 unit tests in [`backend/test_cpcb_calculator.py`](file:///Users/suprith.s.b/Documents/antigravity/DS-hackathon/backend/test_cpcb_calculator.py).
  2. [`backend/data_pipeline.py`](file:///Users/suprith.s.b/Documents/antigravity/DS-hackathon/backend/data_pipeline.py):
     - Processed 50,584 raw daily pollutant observations from XKDR CAAQM archive.
     - Enforced CPCB 16-hour sufficiency filter (46,795 compliant records preserved, 3,789 unrepresentative records dropped).
     - Processed 16,080 hourly ERA5 reanalysis weather records with meteorological vector wind decomposition ($u, v$).
     - Calculated continuous 670-day City Composite AQI (2023-01-01 to 2024-10-31, 100% valid days).
     - Computed Pearson retrospective weather-pollution correlation matrix.
     - Computed landmark 24-hour diurnal curves for BTM Layout and Peenya.
     - Generated 6 validated artifacts in `data/processed/`.
     - Verified by 8 integration tests in [`backend/test_data_pipeline.py`](file:///Users/suprith.s.b/Documents/antigravity/DS-hackathon/backend/test_data_pipeline.py).
  3. [`backend/ml_pipeline.py`](file:///Users/suprith.s.b/Documents/antigravity/DS-hackathon/backend/ml_pipeline.py):
     - Autoregressive next-day forecasting model ($t+1$) with strictly past features at issue time $t$.
     - Zero target-day realized weather leakage.
     - Chronological train (2023-01 to 2024-06) / test (2024-07 to 2024-10) split.
     - Held-out evaluation: Random Forest (MAE 7.68, RMSE 11.03, $R^2$ 0.705) vs Persistence Baseline (MAE 7.42, RMSE 10.49, $R^2$ 0.733) vs 7-day Moving Average (MAE 9.20, RMSE 15.08, $R^2$ 0.449).
     - Serialized to `data/processed/model_evaluation.json`.
  4. [`backend/main.py`](file:///Users/suprith.s.b/Documents/antigravity/DS-hackathon/backend/main.py):
     - FastAPI application serving all 9 REST endpoints with offline in-memory cache.
     - Verified by 9 end-to-end API tests in [`backend/test_api.py`](file:///Users/suprith.s.b/Documents/antigravity/DS-hackathon/backend/test_api.py).
  5. **Total Test Suite:** 60 tests passed with 100% pass rate in 0.20s.
