# Product Requirements Document (PRD)
# Project BreatheWise — Bengaluru Air Quality & Meteorological Intelligence Platform

**Document Version:** 1.2.0 (Pre-Implementation Gate Finalization)  
**Status:** DRAFT FOR FINAL APPROVAL  
**Domain:** Urban Environmental Intelligence / Applied Data Science  
**Target City:** Bengaluru, Karnataka, India  

---

## 1. Product Overview

### 1.1 Problem Statement
Urban air quality in Bengaluru exhibits notable spatial variation across its 14 CPCB monitoring stations, driven by localized traffic corridors, industrial zones, and seasonal meteorological transitions. Citizens, sensitive demographics (people with asthma, children, elderly), and environmental researchers lack an integrated, transparent, offline-capable platform that connects authentic Central Pollution Control Board (CPCB) ambient air measurements with ECMWF ERA5 reanalysis weather data to deliver standard IND-AQI calculations, station-level spatial insights, honest historical next-day forecast backtesting without target weather leakage, and CPCB-grounded health advisories.

### 1.2 Target Users & Needs
1. **Health-Conscious Citizens & Sensitive Demographics:** Need transparent, CPCB-standard health advisories tailored to specific vulnerability profiles without unsupported clinical claims.
2. **Data Science Judges & Environmental Researchers:** Need verifiable data provenance, rigorous CPCB math, chronological validation with zero future data leakage, and honest disclosure of missing station-days.
3. **Urban Commuters:** Need station comparisons, peak diurnal pollution curves (where hourly ground data exists), and retrospective weather-pollution correlation analysis.

---

## 2. Core Functional Requirements

### FR-1: Authentic Multi-Station Ingestion & Spatial Mapping
- Ingest 14 cataloged CPCB/KSPCB CAAQM monitoring stations across Bengaluru:
  * 13 active reporting stations across 2023–2024.
  * 1 decommissioned station: BWSSB Kadabesanahalli (`site_164`, closed Aug 2022; 0 records in 2023–2024, preserved in catalog with `is_active: false`).
- Display verified station metadata: station name, regulatory operator (CPCB vs KSPCB), latitude, longitude, and active monitored parameters.

### FR-2: Official CPCB IND-AQI Calculation Engine (Strictly Bounded)
- Implement the exact mathematical piecewise linear interpolation formula defined in the official CPCB 2014 *National Air Quality Index (IND-AQI)* technical report:
  $$I_p = \left[ \frac{I_{HI} - I_{LO}}{B_{HI} - B_{LO}} \right] \times (C_p - B_{LO}) + I_{LO}$$
- **Concentration Breakpoint vs Sub-Index Separation:**
  * Good ($0 - 50$): $\text{PM}_{10}\ [0, 50]$, $\text{PM}_{2.5}\ [0, 30]$, $\text{NO}_2\ [0, 40]$, $\text{SO}_2\ [0, 40]$, $\text{NH}_3\ [0, 200]$, $\text{Pb}\ [0, 0.5]$
  * Satisfactory ($51 - 100$): $\text{PM}_{10}\ (50, 100]$, $\text{PM}_{2.5}\ (30, 60]$, $\text{NO}_2\ (40, 80]$, $\text{SO}_2\ (40, 80]$, $\text{NH}_3\ (200, 400]$, $\text{Pb}\ (0.5, 1.0]$
  * Moderate ($101 - 200$): $\text{PM}_{10}\ (100, 250]$, $\text{PM}_{2.5}\ (60, 90]$, $\text{NO}_2\ (80, 180]$, $\text{SO}_2\ (80, 380]$, $\text{NH}_3\ (400, 800]$, $\text{Pb}\ (1.0, 2.0]$
  * Poor ($201 - 300$): $\text{PM}_{10}\ (250, 350]$, $\text{PM}_{2.5}\ (90, 120]$, $\text{NO}_2\ (180, 280]$, $\text{SO}_2\ (380, 800]$, $\text{NH}_3\ (800, 1200]$, $\text{Pb}\ (2.0, 3.0]$
  * Very Poor ($301 - 400$): $\text{PM}_{10}\ (350, 430]$, $\text{PM}_{2.5}\ (120, 250]$, $\text{NO}_2\ (280, 400]$, $\text{SO}_2\ (800, 1600]$, $\text{NH}_3\ (1200, 1800]$, $\text{Pb}\ (3.0, 3.5]$
  * Severe ($401 - 500$): $\text{PM}_{10} > 430$, $\text{PM}_{2.5} > 250$, $\text{NO}_2 > 400$, $\text{SO}_2 > 1600$, $\text{NH}_3 > 1800$, $\text{Pb} > 3.5$, $\text{CO} > 34$, $\text{O}_3 > 748$.
- **Project Implementation Policy: Severe Values Reported at 500 Ceiling:**
  * Official CPCB Table 3.2 specifies open-ended concentration ranges for the Severe category ($401–500$) without publishing upper concentration limits ($B_{HI}$).
  * CPCB guidelines provide piecewise linear interpolation for categories 1–5, but do not prescribe an official interpolation formula beyond the Severe lower boundary.
  * In BreatheWise, assigning a sub-index of **500.0** when $C_p > B_{LO, \text{severe}}$ is an **explicit project implementation policy** reflecting the CPCB official national index ceiling, NOT an officially prescribed CPCB linear interpolation formula.
  * Furthermore, readings exceeding the physical measurement range of standard CAAQM analyzers ($>1000\ \mu\text{g/m}^3$) are treated as instrument saturation faults.
  * Rigorously verified in automated test suite [`scripts/test_cpcb_calculator.py`](file:///Users/suprith.s.b/Documents/antigravity/DS-hackathon/scripts/test_cpcb_calculator.py).
- **CO and O3 Averaging Protocol:**
  * CPCB specifies 8-hour averaging for CO and $\text{O}_3$.
  * Because the daily harvested archive (`bengaluru_daily_combined_raw.json`) provides 24-hour daily arithmetic means, **CO and $\text{O}_3$ sub-indices are strictly excluded from daily station AQI calculations** to prevent substituting daily means for 8-hour metrics.
  * Station AQI is calculated using the five genuine 24-hour criteria pollutants ($\text{PM}_{2.5}, \text{PM}_{10}, \text{NO}_2, \text{SO}_2, \text{NH}_3$), satisfying CPCB’s 3-pollutant requirement.
  * In landmark hourly datasets (BTM Layout & Peenya), rolling 8-hour averages are computed using a **project-defined completeness threshold of at least 6 of 8 valid hourly observations (75%)**. Windows with $<6$ observations are marked invalid.
- **16-Hour Sufficiency Rule:** Daily records with $n < 16$ hours are excluded from AQI calculations.
- **Worst-Pollutant Principle:** Station $\text{AQI} = \max_p(I_p)$. Prominent Pollutant is $\arg\max_p(I_p)$.

### FR-3: City Composite AQI Aggregation
- Daily arithmetic mean of reporting active stations' valid AQIs, matching CPCB National Air Quality Daily Bulletin standard.

### FR-4: Environmental Explorer & Historical Station-Specific Diurnal Profiles
- Multi-pollutant daily time-series exploration across 2023–2024.
- **Diurnal Hourly Analysis (Descriptive Station-Specific Findings):**
  * Displays 24-hour diurnal curves strictly for the landmark stations where genuine hourly data exists: BTM Layout (`site_162`) and Peenya (`site_163`) across 4 seasonal benchmark months in 2024 (January, April, July, October; 66,947 observations).
  * Reports descriptive historical patterns without speculative causal claims:
    - At BTM Layout, $\text{NO}_2$ averages are highest during morning hours (07:00–09:00, peaking at $36.33\ \mu\text{g/m}^3$) and lower during midday ($29.67 - 30.67\ \mu\text{g/m}^3$).
    - At both BTM Layout and Peenya, $\text{PM}_{10}$ and $\text{PM}_{2.5}$ averages in the dataset are higher in the late evening (20:00–22:00, $71.84\ \mu\text{g/m}^3$ at BTM, $76.97\ \mu\text{g/m}^3$ at Peenya) than during midday (12:00–16:00, $46.78\ \mu\text{g/m}^3$ at BTM), with a secondary morning peak at 08:00–09:00 ($65.49\ \mu\text{g/m}^3$).
  * Clearly labeled as historical observations specific to BTM Layout and Peenya, not city-wide generalizations.

### FR-5: Retrospective Meteorological Correlation (No Leakage)
- Evaluates surface ventilation and precipitation wet scavenging using ECMWF ERA5 reanalysis surface data (temperature, humidity, precipitation, orthogonal $u, v$ wind vectors, surface pressure).
- Labeled explicitly as **Retrospective Historical Correlation Analysis**, strictly separated from forecasting.

### FR-6: Honest Autoregressive Next-Day Forecasting (Zero Weather Leakage)
- **No Target-Day Weather Leakage:** The forecasting model uses **ONLY information available at prediction issue time $t$**:
  * Autoregressive lags: $\text{PM2.5}_t, \text{PM2.5}_{t-1}, \text{PM2.5}_{t-2}, \text{PM10}_t, \text{PM10}_{t-1}, \dots$
  * Past 3-day and 7-day rolling statistics up to day $t$.
  * Realized weather up to day $t$.
  * Calendar indicators of day $t+1$.
  * **ZERO realized weather from day $t+1$ is provided to the model.**
- **Chronological Split:** Train strictly on 2023-01-01 to 2024-06-30; evaluated on held-out historical test window (2024-07-01 to 2024-10-31).
- **Baselines:** Persistence Baseline ($\text{AQI}_{t+1} = \text{AQI}_t$) and 7-day Moving Average.

### FR-7: CPCB-Grounded Health Advisory
- 100% aligned with the 6 official CPCB risk tiers.
- Presents observed diurnal peak hours as historical station-specific patterns from BTM Layout and Peenya, avoiding universal medical advice or citywide mandates.

### FR-8: Data Transparency & Audit Ledger
- Full audit documenting 60,970 expected vs 50,584 actual records (82.97% density), 10,386 missing combinations, and $n \ge 16$ sufficiency filter.

### FR-9: Scenario Explorer (Optional / Experimental)
- Kept out of the critical MVP implementation path. Evaluated only as a secondary experimental tool with input domain validation.
