# BreatheWise — Judge Technical Q&A Defense Ledger

This document contains 22 rigorous technical and architectural questions likely to be asked by hackathon judges, paired with concise, scientifically defensible answers.

---

### Core Questions Judges Will Ask

#### Question 1: Why does your Random Forest perform worse than persistence?
> **Answer:** The model was evaluated on a chronological held-out test period (July 1 to October 31, 2024). Persistence achieved an MAE of 7.42, while the direct AQI Random Forest achieved 7.74 and the two-stage physical model achieved 7.91. Our evaluation showed that the simple persistence baseline outperformed both machine-learning approaches on the held-out test period. We report this honestly rather than claiming ML superiority. It demonstrates why complex models must be tested against simple baselines before claiming predictive value.

#### Question 2: Is your AQI data live?
> **Answer:** No. The latest available observation is October 31, 2024. The application is a historical intelligence and analysis platform, not a real-time AQI service. We explicitly disclose this limitation in our header banner and across the documentation.

#### Question 3: How do you calculate AQI?
> **Answer:** We use CPCB Table 3.2 breakpoint interpolation for the defined concentration ranges (categories 1–5, 0–400 AQI). The station AQI is governed by the worst-pollutant principle: the maximum valid pollutant sub-index, subject to CPCB's minimum three-pollutant requirement with at least one particulate pollutant ($\text{PM}_{2.5}$ or $\text{PM}_{10}$). For the open-ended Severe category, we apply an explicitly documented project reporting policy capping at 500.

#### Question 4: Why did you exclude CO and O3 from daily AQI?
> **Answer:** Their daily records are 24-hour arithmetic means, whereas CPCB specifies 8-hour rolling averages for these pollutants. Substituting one for the other would be scientifically and regulatorily incorrect. We evaluate 8-hour rolling CO and $\text{O}_3$ metrics separately on high-resolution landmark hourly observations.

#### Question 5: Does correlation prove weather causes pollution changes?
> **Answer:** No. Pearson correlation measures linear association. It does not establish causation. Confounding variables like seasonal temperature inversions and traffic patterns operate concurrently. Our weather analysis is retrospective and observational, and we maintain non-causal phrasing throughout.

#### Question 6: What happens if the internet is disconnected?
> **Answer:** The application uses local processed datasets, a local FastAPI backend, and locally served frontend assets. It is designed to continue operating without external network access after installation. It is verified 100% offline.

---

### Category 1: Problem Framing, Urban Context & Innovation

#### Q7: Why should I use BreatheWise instead of an existing AQI dashboard?
> **Answer:** Most AQI dashboards focus on reporting an air-quality number. BreatheWise focuses on understanding the data behind that number: how pollutant patterns change over time, how historical weather conditions are associated with them, how different forecasting methods perform, and how the calculations and data limitations can be audited. It combines exploration, evaluation and transparency in one offline-capable platform.

#### Q8: How does BreatheWise handle Bengaluru's geographic and spatial variability?
> **Answer:** The project uses multiple monitoring stations (13 active stations) to explore spatial differences in historical pollution observations across Bengaluru. Its hourly and weather analyses have more limited geographic coverage (hourly data from BTM Layout and Peenya; weather from a single ERA5 coordinate), which we explicitly disclose rather than claiming a complete spatial microclimate model.

#### Q9: Why choose the XKDR CAAQM archive and ECMWF ERA5 rather than commercial scraping?
> **Answer:** Commercial consumer APIs frequently aggregate, smooth, or interpolate data using proprietary black-box algorithms, and often lack raw pollutant concentrations or sensor metadata. XKDR Forum provides direct, raw, unmanipulated CAAQM recordings from CPCB and KSPCB stations under India's Government Open Data License (GODL). ECMWF ERA5 is the gold-standard atmospheric reanalysis produced by physical assimilation of satellite, radar, and weather station readings.

#### Q10: Why are there 14 stations in your catalog but only 13 active stations?
> **Answer:** Station `site_164` (BWSSB Kadabesanahalli) was permanently decommissioned by CPCB in August 2022. Rather than discarding it or fabricating synthetic readings, our pipeline catalogs it with `is_active: false` and displays it with a clear "Decommissioned Aug 2022" badge. The remaining 13 active stations provided between 457 and 632 days of valid data across 2023–2024.

---

### Category 2: CPCB Methodology & Regulatory Compliance

#### Q11: How do you handle the open-ended Severe category in CPCB Table 3.2?
> **Answer:** We maintain three clear distinctions:
> 1. CPCB Table 3.2 provides open-ended Severe concentration thresholds (e.g., $\text{PM}_{2.5} > 250\ \mu\text{g/m}^3$).
> 2. The project reports Severe values at the 500 ceiling as an **explicitly documented implementation policy**.
> 3. We do **not** claim an official CPCB linear interpolation formula beyond the Severe breakpoint, nor do we invent unverified upper concentration breakpoints. This demonstrates regulatory transparency rather than hiding a methodology boundary.

#### Q12: What is your 8-hour rolling completeness rule, and is it an official CPCB formula?
> **Answer:** On our benchmark hourly datasets (BTM Layout and Peenya), we evaluate 8-hour rolling windows using a **project-defined completeness threshold of at least 6 valid hourly readings out of 8 (75%)**. While CPCB mandates an 8-hour averaging window, the 6-of-8 hour threshold is a project-defined quality filter. In our empirical audit across 11,632 possible windows, **10,677 windows (91.8%)** met this requirement.

#### Q13: What is the CPCB 16-hour sufficiency rule, and what impact did it have on your data?
> **Answer:** CPCB guidelines mandate that a valid daily average requires at least 16 hours of continuous monitoring (66.7% daily temporal completeness). In our pipeline, every daily record with $n < 16$ was filtered out. Across our 50,584 raw records, this preserved **46,795 compliant records** and dropped **3,789 unrepresentative records**, ensuring that calculated station AQIs reflect genuine full-day exposure.

---

### Category 3: Atmospheric Physics & Meteorological Analysis

#### Q14: Why did you decompose wind speed and direction into $u$ and $v$ vectors?
> **Answer:** Wind direction is angular ($0^\circ–360^\circ$). Taking a simple arithmetic average of wind direction angles produces mathematically invalid results—for example, averaging $350^\circ$ (NNW) and $10^\circ$ (NNE) yields $180^\circ$ (due South), which is exactly opposite to the physical airflow! By decomposing hourly speed and direction into orthogonal zonal ($u = -ws\sin\theta$) and meridional ($v = -ws\cos\theta$) components, averaging $u$ and $v$, and reconstructing resultant speed and direction, we maintain physical vector integrity.

#### Q15: What did your diurnal analysis discover about commuter patterns?
> **Answer:** Using 66,947 seasonal hourly observations across BTM Layout and Peenya, we found that $\text{NO}_2$ exhibits a morning peak (07:00–09:00, averaging $\approx 36\ \mu\text{g/m}^3$), consistent with vehicular transit windows. Particulate matter exhibits dual elevation: a secondary morning bump and a substantial late-evening elevation (20:00–23:00, averaging $\approx 72–77\ \mu\text{g/m}^3$), with lowest concentrations during midday (12:00–16:00). We report these as descriptive station-specific findings.

---

### Category 4: Machine Learning & The Forecast Arena

#### Q16: How did you ensure zero data leakage in your forecasting pipeline?
> **Answer:** We implemented three strict safeguards:
> 1. **Chronological Splitting:** Training data spans January 8, 2023 to June 30, 2024; the held-out test set spans July 1, 2024 to October 31, 2024 (123 calendar days). Zero shuffling across time.
> 2. **Causal Issue-Time Features:** All features are strictly evaluated at issue time $t$ (past AQI lags, past pollutant lags, rolling statistics, and past realized weather at time $t$).
> 3. **Withheld Target-Day Weather:** Zero target-day ($t+1$) realized ERA5 weather was provided to the models.

#### Q17: Why did you evaluate both a Direct AQI model and a Two-Stage Physical model?
> **Answer:** Our PRD designed a Two-Stage Physical model: predict physical $\text{PM}_{2.5}$ and $\text{PM}_{10}$ concentrations in $\mu\text{g/m}^3$, then pass them through the deterministic CPCB formula. We also evaluated Direct AQI regression. In our held-out test evaluation, Direct RF scored MAE 7.74 ($R^2 = 0.699$) while the Two-Stage Physical model scored MAE 7.91 ($R^2 = 0.625$). The two-stage model preserves physical mass-balance interpretability, while direct regression is slightly smoother. We present both in our Forecast Arena.

#### Q18: Why did the 7-day Moving Average perform worse (MAE 9.20)?
> **Answer:** A 7-day trailing moving average carries significant phase lag. During seasonal transitions (such as Bengaluru's monsoon withdrawal in September and post-monsoon dry onset in October), a 7-day rolling mean systematically lags behind rising particulate trends and falling clean spells.

---

### Category 5: Engineering & Offline Operations

#### Q19: What automated test coverage protects your application against regressions?
> **Answer:** We maintain **60 automated tests** across three test suites (`backend/test_cpcb_calculator.py`, `backend/test_data_pipeline.py`, `backend/test_api.py`) passing in **0.20 seconds**:
> - **43 tests** on CPCB piecewise interpolation, boundaries, Severe ceiling, negative values, and station constraints.
> - **8 tests** on data pipeline sufficiency counts, date continuity, AQI boundedness, and correlation bounds.
> - **9 tests** on REST API endpoints and response schemas.

#### Q20: Why choose React + Vite + Tailwind CSS instead of Streamlit or Dash?
> **Answer:** While Streamlit is common in hackathons, it re-executes the entire script on every user interaction, causing sluggish multi-tab navigation, difficult state management, and limited styling control. A decoupled React + Vite SPA provides instant client-side tab switching, custom interactive Recharts visualizations, fine-grained accessibility, and startup-grade UI tokens adhering to Google Stitch design principles.

---

### Category 6: Product Limitations & Future Roadmap

#### Q21: What are the primary technical limitations of the current prototype?
> **Answer:**
> 1. **Temporal Boundary:** Ground-truth data ends on October 31, 2024; real-time streaming requires active ongoing CPCB telemetry scraping.
> 2. **Spatial Geographic Coverage:** We display station-specific point observations from 13 active stations. Weather data is from a single Bengaluru coordinate, and hourly diurnal data covers two landmark stations (BTM Layout and Peenya).
> 3. **CO/O3 Aggregation:** Excluded from daily AQI due to 24h arithmetic mean limitations in the harvested archive; evaluating 8-hour rolling metrics universally requires citywide hourly feeds.

#### Q22: What future work is planned beyond this prototype?
> **Answer:** *(Note: Clearly identified as future work — not implemented in this prototype)*
> 1. **Spatial Kriging / Interpolation (Future Work):** Exploring continuous concentration heatmaps, subject to empirically validating whether 13 monitoring stations provide adequate spatial density.
> 2. **NWP Weather Forecast Coupling (Future Work):** Testing whether ingesting 24-hour weather predictions (e.g., GFS wind shifts) provides predictive signal beyond persistence.
> 3. **Automated Citizen Notifications (Future Work):** Investigating webhook-based SMS/WhatsApp alerts for school athletics and vulnerable citizen cohorts.
