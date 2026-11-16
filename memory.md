# BreatheWise --- Project Memory and Decision Log

## Current identity

-   Project: BreatheWise.
-   Official track/topic: DS05 --- Air Quality and Weather Patterns.
-   Initial geography: Bengaluru, Karnataka, India.
-   Concept approved by Suprith.
-   Active builders: Suprith and Uday.
-   Team maximum: four. Two additional teammates are expected to
    explain/present the idea and procedure; actual contribution
    descriptions must remain truthful.
-   Eight-hour hackathon plan.

## Approved concept

A platform to explore real air-quality and weather observations,
identify historical/seasonal patterns, analyze pollutant-weather
associations, detect unusual pollution periods, and provide explainable
short-term PM2.5 forecasting if the data supports it.

Distinctive feature: Pollution Pattern Explainer. It should summarize
actual recent trends, pollutant context, weather associations, and
forecast uncertainty. It must not claim causation.

## Organizer permissions reported

-   AI tools allowed.
-   External APIs allowed.
-   Datasets allowed.
-   Prebuilt code allowed.
-   External development tools allowed.
-   Maximum team size four. Still unknown: submission format, deadline,
    judging criteria, demo duration, deployment requirement, repository
    requirements, and team contribution declaration rules.

## Data candidates

### Peenya CPCB 15-minute 2024--25 CSV

Catalogue:
https://data.opencity.in/dataset/bengaluru-hourly-air-quality-reports
Resource:
https://data.opencity.in/dataset/bengaluru-hourly-air-quality-reports/resource/c6b4282e-43c8-4f14-a855-83e4b52a80d7
Original CSV:
https://data.opencity.in/dataset/79fa909a-38f1-4657-b369-6d0e2a6f500e/resource/c6b4282e-43c8-4f14-a855-83e4b52a80d7/download/blr-peenya-cpcb-2024-25.csv
Published metadata: CSV, ~11.1 MiB, Public Domain, active datastore; 29
listed fields including timestamp, pollutants, temperature, RH, wind,
rainfall, solar radiation and pressure. **Important:** metadata
inspected; actual CSV contents not yet inspected. Do not call it the
final dataset until downloaded and validated.

### OpenAQ Jayanagar 5th Block

https://explore.openaq.org/locations/6973 Station explorer lists
KSPCB/CPCB source, reporting since 2018-08-10, with several pollutant
and weather-related sensors. Actual API data extraction and usable
coverage still need checking. API docs: https://docs.openaq.org/api
OpenAQ API v3 uses API key; keep key server-side/environment-only.

### Open-Meteo

Historical weather docs:
https://open-meteo.com/en/docs/historical-weather-api Terms:
https://open-meteo.com/en/terms Historical weather is reanalysis, not
necessarily an on-site station measurement. Free API is for
non-commercial use and requires CC BY 4.0 attribution under published
terms. Check terms before use and show attribution.

## Scientific decisions

-   First candidate target: future PM2.5.
-   Do not promise 72-hour forecast until data continuity and evaluation
    support it.
-   Use chronological train/validation/test split.
-   Compare to persistence/seasonal baseline.
-   Report MAE/RMSE and test period; no invented metrics.
-   AQI must follow CPCB method and pollutant-specific data
    requirements. Do not average concentrations to create AQI.
-   Correlation/feature importance are not causal explanations.
-   If model not reliable, deliver EDA and insights without pretending a
    successful forecast.

## Proposed stack

Python, Pandas, NumPy, Scikit-learn; React + TypeScript + Tailwind;
FastAPI if needed; Plotly/Recharts; local CSV/Parquet; SQLite only if
useful. Prefer simple offline-first architecture.

## Design

Google Stitch: https://stitch.withgoogle.com/ Screens: Overview,
Explorer, Weather Relationships, Forecast & Explanation, Insights.
Initial design exploration max 45 minutes.

## Team split

-   Suprith: product/integration owner; frontend, backend integration,
    UI, system testing, presentation.
-   Uday: data owner; acquisition, validation, cleaning, EDA, modelling,
    evaluation.
-   Both should understand whole product and review integration.
-   Two additional teammates: prepare to explain project context, data,
    method, architecture, demo and limitations; do not misrepresent who
    implemented which component.

## Current status

-   Project plan approved.
-   Rules/PRD/architecture/design/phase/memory drafted.
-   Organizer core permissions reported.
-   Actual dataset not yet inspected.
-   Submission details still unknown.
-   Implementation not started.
-   No EGM review was performed; available tools did not expose a
    verifiable EGM capability. Do not claim otherwise.

## Next actions

1.  Get actual Peenya CSV and inspect it.
2.  If unavailable, retrieve OpenAQ data for a Bengaluru station.
3.  Record organizer submission/judging details.
4.  Complete data quality report.
5.  Lock target, forecast horizon, model, and final architecture.
6.  Then begin implementation and update phase/memory continuously.
