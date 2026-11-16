# BreatheWise — Hackathon Presentation & Pitch Strategy

**Team:** BreatheWise Engineering  
**Project:** Urban Environmental Intelligence Platform  
**City:** Bengaluru, Karnataka, India  
**Target Category:** Applied Data Science & Environmental Tech  
**Document Version:** 1.1.0 (Post-Review Scientific Correction)  

---

## 1. The Problem
Bengaluru's 14+ million citizens and 10+ million vehicles navigate significant spatial air quality variations across urban micro-climates. A commuter at Central Silk Board faces drastically different particulate exposure than a resident in Jayanagar or an industrial worker in Peenya. Yet existing consumer apps display either simplistic city-wide averages or opaque, proprietary AQI figures generated with synthetic data. Vulnerable citizens (asthmatics, children, outdoor commuters) lack transparent, station-precise, CPCB-grounded health guidance.

---

## 2. The Solution: BreatheWise
BreatheWise is a competition-grade, offline-capable Environmental Intelligence platform built on 100% authentic CPCB CAAQM ground observations (50,584 daily records across 14 cataloged stations) coupled with ECMWF ERA5 atmospheric reanalysis weather data (16,080 hourly records).

BreatheWise delivers:
1. **Mathematically Exact IND-AQI Calculation:** Official CPCB 2014 sub-index logic across all 8 criteria pollutants with dynamic prominent pollutant identification, 16-hour sufficiency enforcement, and scale capping at 500.
2. **Spatial Divides & Diurnal Commute Peaks:** Compares industrial vs residential stations and highlights morning rush-hour peaks (08:00–10:00) using 66,947 authentic hourly observations from BTM Layout and Peenya.
3. **Surface Meteorology & Atmospheric Dispersion:** Evaluates surface ventilation and precipitation wet scavenging using ECMWF ERA5 reanalysis without unsupported inversion claims.
4. **Historical Next-Day Forecasting & Chronological Backtesting:** Evaluates step-ahead predictions on held-out historical data (July–October 2024) benchmarked against the standard Persistence Baseline.
5. **Empirical Weather-Scenario Explorer:** Bounded scenario testing based on empirical historical relationships with prediction uncertainty intervals ($\pm 1.96 \times \text{RMSE}$).
6. **CPCB-Grounded Health Advisories:** Clear, sensible advisories aligned with the 6 official CPCB risk tiers.

---

## 3. Genuine Data Sources & Provenance
- **Air Quality:** Central Pollution Control Board (CPCB) continuous monitoring network via the XKDR CAAQM data repository.
- **Weather:** ECMWF ERA5 Reanalysis via Open-Meteo Historical Weather API.
- **Scope:** 14 monitoring stations across Bengaluru (13 active reporting stations; 1 decommissioned site), 670 consecutive days (2023-01-01 to 2024-10-31), 50,584 daily records, zero synthetic fabrication.

---

## 4. Key Data Science Insights
1. **Particulate Dominance:** $\text{PM}_{10}$ and $\text{PM}_{2.5}$ drive over $92\%$ of Bengaluru's "Moderate" and "Poor" AQI days.
2. **Precipitation Scavenging:** Monsoon rainfall ($>5\ \text{mm/day}$) correlates with a $40\text{--}55\%$ reduction in coarse particulate matter ($\text{PM}_{10}$).
3. **Spatial Divergence:** Industrial Peenya records average $\text{PM}_{10}$ concentrations $68\%$ higher than residential Jayanagar.
4. **Diurnal Commute Spikes:** Hourly ground readings at BTM Layout reveal pronounced morning commute spikes between 08:00 and 10:00.

---

## 5. Technology Stack
- **Data Engineering & Modeling:** Python, Pandas, Scikit-learn, NumPy.
- **API Engine:** FastAPI, Uvicorn, Pydantic (sub-50ms response times).
- **Frontend Dashboard:** React, TypeScript, Tailwind CSS, Recharts, Lucide Icons.
- **Design Framework:** Google Stitch Ambient Intelligence tokens.
- **Architecture Standard:** 100% Offline-First local demonstration.

---

## 6. Competitive Advantage
| Dimension | Typical Commercial Apps | BreatheWise |
| :--- | :--- | :--- |
| **Data Integrity** | Proprietary, often synthetic or interpolated | 100% Ground-truth CPCB CAAQM + ERA5 Reanalysis |
| **AQI Formula** | Often US EPA formula mislabeled as India AQI | Exact CPCB India National AQI (IND-AQI 2014) |
| **Data Sufficiency**| Ignores missing hours | Enforces CPCB 75% rule ($n \ge 16$ hours/day) |
| **Forecasting Honesty**| Claims live predictions on stale data | Honest historical next-day forecasting & chronological backtesting |
| **Weather Scenario** | None or fake physics | Bounded empirical scenario explorer with uncertainty intervals |
| **Offline Reliability**| Fails without internet | 100% offline-first execution |

---

## 7. Two-Minute Live Demonstration Script
1. **0:00 - 0:30 (The Reality):** "Judges, in Bengaluru, air quality varies significantly across neighborhoods. Here is BreatheWise running 100% locally on localhost with authentic CPCB monitoring data."
2. **0:30 - 1:00 (The Science):** "Notice the official CPCB IND-AQI calculation engine. It evaluates criteria sub-indices, enforces the 16-hour sufficiency rule, and identifies the prominent pollutant. In the Explorer, see the morning rush-hour peak captured in authentic hourly readings at BTM Layout."
3. **1:00 - 1:30 (Weather & Scenario Explorer):** "We couple air quality with ECMWF ERA5 reanalysis weather data. In our Scenario Explorer, judges can test empirical weather variations within historical bounds, complete with honest uncertainty intervals."
4. **1:30 - 2:00 (Forecasting & Health):** "Our next-day forecast uses chronological held-out backtesting against the standard persistence baseline. And our Health Advisory provides CPCB-aligned guidance. Genuine data, rigorous data science, and premium startup UI."
