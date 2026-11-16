# BreatheWise — 2-Minute Competitive Pitch Script

**Format:** Spoken presentation to hackathon judging panel  
**Target Duration:** 120 seconds (approx. 275 words at steady conversational cadence)  
**Speaker Persona:** 2nd-year CSE Data Science Student / Senior Technical Co-founder  
**Core Theme:** Truthful Data Science, Genuine Data, CPCB Regulatory Integrity, and Transparent Model Benchmarks  

---

### [00:00 – 00:25] Opening Hook, Real Problem & Innovation Value
> "Good morning, judges. Most air quality apps give you a single colored number and tell you to wear a mask. But they hide the actual science, smooth over data gaps, and leave citizens blind to the diurnal patterns that govern real daily exposure.
> 
> Most AQI dashboards focus on reporting an air-quality number. BreatheWise focuses on understanding the data behind that number: how pollutant patterns change over time, how historical weather conditions are associated with them, how different forecasting methods perform, and how the calculations and data limitations can be audited. It combines exploration, evaluation and transparency in one offline-capable platform.
> 
> The project uses multiple monitoring stations to explore spatial differences in historical pollution observations. Its hourly and weather analyses have more limited geographic coverage, which we explicitly disclose."

---

### [00:25 – 00:50] Genuine Data & Regulatory Grounding
> "We began with one non-negotiable rule: **zero synthetic data**.
> 
> We harvested and validated **50,584 daily pollutant observations** from CPCB across 14 Bengaluru monitoring stations, coupled with **16,080 hourly meteorological records** from ECMWF ERA5 reanalysis, and **66,947 seasonal hourly observations** across BTM Layout and Peenya.
> 
> We strictly implemented the official CPCB Table 3.2 piecewise formula. We enforced CPCB's 16-hour sufficiency rule—preserving 46,795 compliant records and discarding 3,789 unrepresentative ones. We separated 24-hour daily means from 8-hour metrics, properly excluding CO and Ozone from daily station AQI. And for Severe values, we instituted an explicit 500 ceiling cap policy without claiming an official CPCB linear interpolation formula beyond the Severe breakpoint."

---

### [00:50 – 01:25] The Forecast Arena & Our Core Scientific Finding
> "When building our next-day forecast, we enforced strict time-series causality—zero future weather leakage. We benchmarked four distinct approaches on a 123-day held-out test set from July to October 2024:
> 
> Here is our core scientific finding:
> **Our evaluation showed that the simple persistence baseline outperformed both machine-learning approaches on the held-out test period. This demonstrates why complex models must be tested against simple baselines before claiming predictive value.**
> 
> Specifically, the simple Persistence baseline scored an **MAE of 7.42 points**, while our Direct Random Forest scored **7.74** and our Two-Stage Physical model scored **7.91**. Both substantially beat a 7-day moving average of 9.20. We show all four models side-by-side in our Forecast Arena with complete scientific transparency. That is real, defensible Data Science."

---

### [01:25 – 01:50] The Working Product & Offline Engineering
> "BreatheWise is not a mockup. It is a live, full-stack product:
> • **Overview:** Displays Bengaluru's composite AQI of 141 (Moderate) on our latest historical date, October 31, 2024, across 13 active stations and 1 decommissioned site.
> • **Explorer:** 670 days of continuous multi-pollutant trends and 24-hour diurnal commute curves.
> • **Health Advisory:** CPCB 6-tier health guidance with vulnerable population safeguards.
> • **Data Transparency:** An interactive CPCB calculator and full audit ledger.
> 
> Backed by **60 automated tests passing in 0.20 seconds**, the entire application runs **100% offline** on localhost."

---

### [01:50 – 02:00] Closing Statement
> "BreatheWise proves that honest data, rigorous regulatory compliance, and transparent machine learning benchmarks deliver far greater value than exaggerated black-box claims.
> 
> Thank you, and we welcome your questions."

---

### Speaker Delivery Notes & Timing Cues
- **00:00 – 00:25 (Problem & Innovation):** Clear, grounded tone. Deliver the differentiation statement with conviction.
- **00:25 – 00:50 (Data & Regulatory):** Highlight the exact numbers (50,584 records, 16h sufficiency). Shows mastery of data engineering.
- **00:50 – 01:25 (Forecast Finding):** Deliver the persistence finding candidly: simple persistence beating ML proves why baselines are essential.
- **01:25 – 01:50 (Product):** Fast, sharp tour of the 5 screens.
- **01:50 – 02:00 (Close):** Strong eye contact with the judging panel.
