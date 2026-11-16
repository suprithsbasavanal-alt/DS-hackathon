# BreatheWise — 3-Minute Judge Demonstration Runbook

**Target Duration:** Exactly 180 seconds (3:00)  
**Setup:** Application live on `http://localhost:8000` (FastAPI daemon serving React frontend)  
**Demonstration Mode:** 100% Offline (Network disabled to prove resilience)  

---

### Step 1: Overview Screen & Data Freshness Warning [00:00 – 00:35] (35s)
- **UI Action:** Open browser to `http://localhost:8000`. Tab: **Overview**.
- **What the Judge Should Notice:** Prominent historical date warning, genuine station coverage, zero fake live data.
- **What to Say:**
  > "Judges, welcome to BreatheWise. Notice immediately our top header banner: we explicitly state that this dataset covers January 2023 to October 31, 2024. We do not make false claims of real-time conditions.
  > 
  > On our latest historical date, October 31, 2024, Bengaluru's composite AQI was **141 (Moderate)**, driven predominantly by coarse dust ($\text{PM}_{10}$).
  > 
  > Here is our 14-day trajectory sparkline leading up to that date, coupled with real ERA5 surface meteorology: 24.2°C temperature, 67% humidity, and 8.4 km/h resultant vector wind.
  > 
  > Below, you can see our multi-station network. 13 stations are active with individual historical observations, and station `site_164` (BWSSB Kadabesanahalli) is clearly badged as Decommissioned in August 2022 rather than pretending it has data. The project uses multiple monitoring stations to explore spatial differences in historical pollution observations, while hourly and weather analyses have more limited geographic coverage, which we explicitly disclose."

---

### Step 2: Explorer — Trends & Diurnal Commuter Curves [00:35 – 01:10] (35s)
- **UI Action:** Click **Explorer** in the top navigation bar.
- **What the Judge Should Notice:** Actual trends, station-specific patterns, non-causal weather associations.
- **What to Say:**
  > "Moving to the Explorer, here is 670 consecutive days of multi-pollutant observations. I can toggle individual pollutants—watch how $\text{PM}_{10}$ and $\text{PM}_{2.5}$ track each other closely, while gaseous $\text{SO}_2$ remains well within national clean standards throughout the year.
  > 
  > To the left, look at our 24-hour diurnal commute curves from 66,947 seasonal hourly observations across BTM Layout and Peenya. At BTM Layout, $\text{NO}_2$ peaks sharply during the morning transit window between 07:00 and 09:00. Particulates show a secondary morning bump and a substantial late-evening elevation between 20:00 and 23:00, with a midday lull.
  > 
  > To the right, our retrospective weather table establishes real atmospheric associations: wind speed correlates negatively with $\text{PM}_{2.5}$ at $-0.263$, and rainfall correlates negatively with $\text{PM}_{10}$ at $-0.431$. We report these strictly as statistical associations, never implying direct causation."

---

### Step 3: Forecast Arena — The Honest 4-Model Comparison [01:10 – 01:55] (45s)
- **UI Action:** Click **Forecast Arena** in the top navigation bar.
- **What the Judge Should Notice:** Four-model comparison, rigorous time-series protocol, and honest persistence benchmark.
- **What to Say:**
  > "Now to the core Data Science module: the Forecast Arena.
  > 
  > At forecast issue time $t$, we strictly enforce zero future data leakage. We evaluated next-day predictions across a 123-day held-out test split from July to October 2024.
  > 
  > Look at our four-model benchmark table:
  > 1. **Persistence Baseline:** MAE = 7.42 points ($R^2 = 0.733$).
  > 2. **Direct AQI Random Forest:** MAE = 7.74 points ($R^2 = 0.699$).
  > 3. **Two-Stage Physical Model:** MAE = 7.91 points ($R^2 = 0.625$).
  > 4. **7-Day Moving Average:** MAE = 9.20 points ($R^2 = 0.449$).
  > 
  > Notice that our Random Forest models do not beat persistence. Our evaluation showed that the simple persistence baseline outperformed both machine-learning approaches on the held-out test period. This demonstrates why complex models must be tested against simple baselines before claiming predictive value.
  > 
  > In the interactive timeline below, you can toggle between models and see how each tracks actual observations across all 123 test days without synthetic smoothing."

---

### Step 4: Health Advisory Screen [01:55 – 02:25] (30s)
- **UI Action:** Click **Health Advisory** in the top navigation bar.
- **What the Judge Should Notice:** CPCB categories, sensitive group advice, and clear non-medical boundaries.
- **What to Say:**
  > "In the Health Advisory screen, we translate index values into official CPCB 6-tier health categories.
  > 
  > Clicking between tiers dynamically reveals general citizen advice alongside targeted safeguards for vulnerable groups: asthmatics, children, and outdoor delivery workers.
  > 
  > We combine this with our empirical commute findings: advising asthmatics to shift strenuous workouts away from late evening peak particulate hours, while clearly noting this is descriptive station evidence rather than generalized medical prescription."

---

### Step 5: Data Transparency & Interactive Calculator [02:25 – 02:50] (25s)
- **UI Action:** Click **Data Transparency** in the top navigation bar.
- **What the Judge Should Notice:** Real-time CPCB Table 3.2 calculator, 500 ceiling policy, and 16-hour sufficiency audit.
- **What to Say:**
  > "Finally, our Data Transparency screen and audit ledger.
  > 
  > Here are the exact numbers: 50,584 raw records ingested, 46,795 compliant records preserved under CPCB's 16-hour sufficiency rule, and 3,789 unrepresentative records dropped.
  > 
  > And here is our live CPCB Table 3.2 calculator widget: if I enter 75 µg/m³ for $\text{PM}_{2.5}$, it calculates an exact sub-index of 150.5 in Moderate. If I enter an extreme spike of 260 µg/m³, it enforces our project implementation policy, reporting at the 500 ceiling cap. CPCB Table 3.2 provides open-ended Severe thresholds, and we explicitly document this 500 ceiling as an implementation policy rather than claiming an official CPCB interpolation formula."

---

### Step 6: Closing & One-Sentence Value Proposition [02:50 – 03:00] (10s)
- **What the Judge Should Notice:** Clear, compelling value proposition that defines why BreatheWise matters.
- **What to Say:**
  > "Most AQI dashboards focus on reporting an air-quality number. BreatheWise focuses on understanding the data behind that number: combining exploration, evaluation and transparency in one offline-capable platform.
  > 
  > Thank you, judges. We are ready for your questions."
