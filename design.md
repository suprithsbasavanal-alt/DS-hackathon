# UI/UX Design System Specification
# Project BreatheWise — Google Stitch Design Architecture

**Design System:** Google Stitch Ambient Intelligence  
**Aesthetic Standard:** Modern, technical, clean, dark-mode first with high-contrast accessibility  
**Framework:** React, TypeScript, Tailwind CSS, Lucide Icons, Recharts  
**Document Version:** 1.2.0 (Pre-Implementation Gate Finalization)  

---

## 1. Design Tokens & Visual Hierarchy

### 1.1 Color Palette
The color system is anchored around atmospheric clarity and official CPCB AQI hazard tiers.

- **Background & Canvas:**
  * Background Default: `#0B0F19` (Deep Atmospheric Navy)
  * Card Surface: `#111827` (Charcoal Slate)
  * Elevated Surface / Hover: `#1F2937` (Cool Gray Slate)
  * Border / Hairline: `#374151` (Subtle 1px border)

- **Typography & Foreground:**
  * Primary Text: `#F9FAFB` (Pure High-Contrast White)
  * Secondary Text: `#9CA3AF` (Muted Metallic Gray)
  * Tertiary / Labels: `#6B7280` (Deep Cool Gray)
  * Accent / Brand: `#38BDF8` (Atmospheric Sky Blue)

- **Official CPCB AQI Category Colors:**
  * Good (0–50): `#10B981` (Emerald Green)
  * Satisfactory (51–100): `#84CC16` (Bright Lime Green)
  * Moderate (101–200): `#F59E0B` (Amber Orange)
  * Poor (201–300): `#EF4444` (Coral Red)
  * Very Poor (301–400): `#8B5CF6` (Vivid Purple)
  * Severe (401–500): `#991B1B` (Deep Maroon Crimson)

### 1.2 Typography
- **Primary Font Family:** Inter / System Sans-serif (`font-sans`)
- **Monospace (Data / Values):** JetBrains Mono / SF Mono (`font-mono`)

---

## 2. Navigation & Layout Architecture

### Global Top Header
- **Left:** BreatheWise logo (wind motif) + City indicator ("Bengaluru • 13 Active CAAQM Stations").
- **Center:** Navigation Tabs:
  1. `Overview`
  2. `Explorer`
  3. `Forecast (Backtest)`
  4. `Health Advisory`
  5. `Data Transparency`
- **Right:**
  * Offline Status Badge: `🟢 100% Offline Ready • Local Engine`
  * (Optional) Action: `Experimental Scenario Explorer` button.

---

## 3. Screen Specifications & Wireframe Blueprints

### Screen 1: City Overview (Command Center)
- **Data Banner:** Clearly displays: *"Latest Available Historical Observations: October 31, 2024 • 13 Active Reporting CAAQM Stations"*.
- **Hero Grid (Top Row):**
  * **Card 1: City Composite AQI Speedometer:** Renders arithmetic average of reporting stations' valid AQIs on the date, with CPCB color tier and prominent pollutant pill.
  * **Card 2: Prominent Pollutant Breakdown:** Comparative bar showing $\text{PM}_{10}$ vs $\text{PM}_{2.5}$ vs $\text{NO}_2$ sub-indices driving the maximum index.
  * **Card 3: Surface Weather Snapshot:** Latest ERA5 surface reanalysis parameters: Temperature ($^\circ\text{C}$), Humidity ($\%$), Wind Speed & Direction, Surface Pressure.
  * **Card 4: Instant CPCB Health Category Summary:** Immediate official CPCB guidance for today's tier.
- **Station Grid (Middle Row):**
  * Grid of 13 active station cards showing station name, regulatory operator (CPCB/KSPCB), current AQI category, prominent pollutant, and 7-day sparkline.
  * Sector Filter Chips: *All (13), South (Silk Board, BTM, Jayanagar), North (Hebbal, Kasturi Nagar), West (Peenya, Bapuji Nagar), Central (City Station)*.
  * Decommissioned station (`site_164` Kadabesanahalli) is cleanly badged as *Decommissioned (Aug 2022)* and excluded from active cards.
- **30-Day City Trend:**
  * Area chart of historical daily city composite AQI over the final 30 days of the dataset.

### Screen 2: Deep-Dive Explorer
- **Station & Pollutant Selectors:**
  * Station dropdown (13 active stations).
  * Pollutant toggle chips ($\text{PM}_{2.5}, \text{PM}_{10}, \text{NO}_2, \text{SO}_2, \text{NH}_3$).
- **Multi-Pollutant Historical Series:**
  * Synchronized time series over 2023–2024 with seasonal shading (Monsoon: June–September).
- **Hourly Landmark Profile (Statistically Validated):**
  * Displays authentic 24-hour diurnal curves for landmark stations where genuine hourly data exists: BTM Layout (`site_162`) and Peenya (`site_163`) across 4 seasonal benchmark months in 2024 (January, April, July, October; 66,947 observations).
  * Reflects verified empirical findings:
    - $\text{NO}_2$ peaks during morning rush hour (07:00–09:00).
    - Particulate matter ($\text{PM}_{10}, \text{PM}_{2.5}$) and $\text{CO}$ peak during late evening/night (20:00–23:00) with a secondary morning rush-hour peak (08:00–09:00).
    - Midday minimums (12:00–16:00) due to solar convective mixing.
- **Retrospective Weather Correlation Heatmap:**
  * Correlation matrix showing empirical associations between ERA5 surface meteorology and pollutant concentrations. Labeled as retrospective analysis.

### Screen 3: Autoregressive Forecasting Arena (Zero Weather Leakage)
- **Header Banner:** *"Autoregressive Next-Day Forecasting & Chronological Backtesting • Held-Out Test Window: July 1 to October 31, 2024 • Strict Cutoff at Time t"*.
- **Performance Evaluation Cards (Loaded dynamically from `data/processed/model_evaluation.json`):**
  * **Persistence Baseline ($\text{AQI}_{t+1} = \text{AQI}_t$):** Live MAE, RMSE, and $R^2$ on held-out test data.
  * **Autoregressive Pooled Model:** Live MAE, RMSE, and $R^2$ with error reduction percentage over baseline.
- **Observed vs Forecast vs Persistence Time-Series Chart:**
  * Synchronized line chart over the 123-day held-out test period comparing actual ground-truth AQI against next-day autoregressive predictions and persistence baseline.

### Screen 4: Health Advisory (CPCB Standard)
- **CPCB Health Risk Categories Panel:**
  * Clearly defines the 6 official CPCB risk tiers with health descriptions.
- **User Profile Guidelines (CPCB Grounded):**
  * 4 targeted user profiles: General Public, Asthmatics, Children/Elderly, Outdoor Commuters.
  * Practical timing advice grounded in verified diurnal findings: recommending avoiding high-exertion outdoor activity during peak evening traffic (20:00–22:00) and morning rush hours (07:00–09:00).

### Screen 5: Data Transparency & Audit Ledger
- **Dataset Provenance Section:**
  * CPCB CAAQM network via XKDR Forum API; ECMWF ERA5 Reanalysis via Open-Meteo.
- **Network Completeness Metrics:**
  * 14 cataloged stations (13 active, 1 decommissioned).
  * Expected combinations: 60,970; Actual combinations: 50,584 (82.97% density); 10,386 unobserved station-days.
  * CPCB 16-Hour Sufficiency: 46,795 records compliant ($n \ge 16$, 92.5%) vs 3,789 filtered out ($n < 16$, 7.5%).
  * Protocol note: CO and $\text{O}_3$ excluded from daily station AQI to avoid substituting 24h daily means for 8h metrics.
- **Interactive CPCB Formula & Unit Test Evidence:**
  * Interactive calculator demonstrating the exact piecewise linear interpolation math and Severe 500-cap ceiling.
  * Displays unit test evidence verifying 100% boundary compliance.

---

## 4. (Optional / Experimental) Weather-Scenario Explorer

- **Status:** Secondary experimental tool; not in the critical MVP path.
- **Input Domain Validation Guards:**
  * Temperature Delta: $\pm 5^\circ\text{C}$ (clamps between $12^\circ\text{C}$ and $39^\circ\text{C}$).
  * Wind Speed Delta: $-8\ \text{km/h}$ to $+15\ \text{km/h}$ (clamps between $2\ \text{km/h}$ and $35\ \text{km/h}$).
  * Precipitation Delta: $0\ \text{mm}$ to $+30\ \text{mm}$.
- **Output:** Point estimate based on empirical historical analogs with explicit prediction interval and mechanism narrative.
