# BreatheWise --- Technical Architecture

**Status:** Proposed; must be updated to match the implementation.

## 1. Architecture principles

-   Offline-first for the judge demo.
-   Simple monolithic architecture; avoid microservices.
-   Reproducible data processing.
-   Clear separation of observed, reanalysis, modelled, and forecast
    data.
-   No secrets in source control.
-   Build a working vertical slice before adding advanced features.

## 2. Logical architecture

``` mermaid
flowchart TD
    A["CPCB / OpenCity CSV"] --> D["Ingestion"]
    B["OpenAQ API or export"] --> D
    C["Open-Meteo historical weather"] --> D
    D --> E["Raw data archive"]
    E --> F["Validation and cleaning"]
    F --> G["Time / station alignment"]
    G --> H["Clean analytical dataset"]
    H --> I["EDA and statistics"]
    H --> J["Feature engineering"]
    J --> K["Baseline and ML evaluation"]
    J --> L["Anomaly detection"]
    K --> M["Saved model and evaluation"]
    I --> N["Application service / API"]
    L --> N
    M --> N
    N --> O["BreatheWise UI"]
```

## 3. Proposed repository structure

``` text
breathewise/
├── rules.md
├── PRD.md
├── architecture.md
├── design.md
├── phase.md
├── memory.md
├── README.md
├── PITCH.md
├── .env.example
├── .gitignore
├── data/
│   ├── raw/              # Original downloads; do not edit
│   ├── processed/        # Reproducible cleaned outputs
│   └── cache/            # Genuine API cache with timestamps
├── notebooks/             # Optional EDA notebooks
├── scripts/
│   ├── inspect_data.py
│   ├── clean_data.py
│   └── train_model.py
├── models/                # Saved model and preprocessing pipeline
├── backend/
│   └── app/
├── frontend/
└── tests/
```

Do not create empty folders/files solely to imitate this tree. Adjust to
the chosen stack and deadline.

## 4. Data ingestion

### Primary candidate

OpenCity catalogue:
https://data.opencity.in/dataset/bengaluru-hourly-air-quality-reports

Peenya CPCB 15-minute 2024--25 resource:
https://data.opencity.in/dataset/bengaluru-hourly-air-quality-reports/resource/c6b4282e-43c8-4f14-a855-83e4b52a80d7

Original CSV URL:
https://data.opencity.in/dataset/79fa909a-38f1-4657-b369-6d0e2a6f500e/resource/c6b4282e-43c8-4f14-a855-83e4b52a80d7/download/blr-peenya-cpcb-2024-25.csv

Metadata reports CSV format, approximately 11.1 MiB, Public Domain
licence, and active datastore. The metadata lists 29 fields. This does
not prove the downloaded file is complete or fit for forecasting.

### Alternative / supplementary

-   OpenAQ station explorer: https://explore.openaq.org/locations/6973
    (Jayanagar 5th Block, Bengaluru --- KSPCB).
-   OpenAQ API documentation: https://docs.openaq.org/api
-   OpenAQ measurements documentation:
    https://docs.openaq.org/resources/measurements
-   Open-Meteo historical weather docs:
    https://open-meteo.com/en/docs/historical-weather-api

## 5. Data processing

1.  Save raw download unchanged.
2.  Record URL, retrieval timestamp, file size, and checksum.
3.  Inspect schema, dtypes, date range, station and time zone.
4.  Parse timestamps and convert to a single documented time zone
    (Asia/Kolkata for local station views).
5.  Convert pollutant/weather columns to numeric safely; log conversion
    failures.
6.  Check duplicates, out-of-range values, missingness, flatlines,
    irregular sampling, and sensor outages.
7.  Do not silently drop or impute values.
8.  Aggregate only after confirming expected sampling and appropriate
    aggregation.
9.  Keep a data-quality report and a reproducible processed file.

## 6. Weather alignment

If external weather reanalysis is used: - Match latitude/longitude and
timestamps. - Document spatial resolution and reanalysis source. -
Reanalysis is not the same as an on-site weather sensor. - Do not use
future observed weather as an input to a real future forecast. - If only
historical reanalysis is available, use it for historical association
analysis, not as if future actual weather were known.

The candidate Peenya CSV already lists weather-related columns. Inspect
these first before adding an external weather source.

## 7. Modelling

Candidate target: PM2.5 at a defined future horizon, selected after
inspecting data frequency and continuity.

Candidate features: - Lagged PM2.5. - Rolling mean/median/std using
past-only windows. - Hour, day-of-week, month. - Temperature, relative
humidity, wind speed/direction, rainfall, pressure when valid. - Other
pollutant readings only if available at prediction time.

Evaluation: - Chronological train/validation/test split. - No random
shuffle. - No target leakage. - Baseline: persistence and/or seasonal
baseline. - Candidate: RandomForestRegressor or
HistGradientBoostingRegressor. - Metrics: MAE and RMSE, with test dates
and sample count. - Save preprocessing and model together. - Do not
claim the model is useful unless it improves meaningfully over baseline
and passes sanity checks.

## 8. AQI handling

If official Indian AQI is shown, implement CPCB methodology with
pollutant-specific breakpoints, averaging periods, and minimum data
requirements. Overall AQI is the maximum valid sub-index, not a mean of
concentrations. If required data is missing, show pollutant
concentrations and clearly state official AQI is unavailable.

CPCB reference: https://cpcb.nic.in/National-AQI/

## 9. Backend/API proposal

Use FastAPI only if a separate backend materially helps.

Potential read-only endpoints: - `GET /api/health` -
`GET /api/metadata` -
`GET /api/observations?station=...&pollutant=...&from=...&to=...` -
`GET /api/summary?...` - `GET /api/correlations?...` -
`GET /api/anomalies?...` - `GET /api/forecast?...`

Return explicit units, timestamps, source type, and errors. Validate all
query parameters.

## 10. Frontend

Proposed pages: - Overview - Explorer - Weather Relationships - Forecast
& Explanation - Insights

All charts must have labels, units, time zones, and source context.
Filters must update real data. Provide loading, empty, and error states.

## 11. Offline strategy

-   Bundle/cache genuine raw and processed data as permitted.
-   Bundle saved model and preprocessing pipeline.
-   Start app without making network calls for core demo.
-   Mark cached timestamps.
-   Provide optional refresh with graceful failure.
-   Test by disabling network before final rehearsal.

## 12. Security

-   OpenAQ API key in environment variable, never frontend.
-   `.env.example` contains placeholders only.
-   `.gitignore` excludes `.env`, local virtual environments, caches,
    and private credentials.
-   No personal or sensitive user data is needed for this project.

## 13. Deployment

Local execution is the reliable default. Public deployment is optional
until organizers confirm it is required and there is time to test it.
Never sacrifice the local demo for deployment.

## 14. Architecture decisions to revisit

-   Final dataset/station and data frequency.
-   Whether weather fields inside the Peenya file are sufficient.
-   Whether external API is needed.
-   Forecast horizon and model choice.
-   React + FastAPI versus simpler single-app architecture.
