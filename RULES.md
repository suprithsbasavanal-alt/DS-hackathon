# BreatheWise --- Permanent Project Rules

**Project:** BreatheWise --- Air Quality & Weather Intelligence\
**Track:** Data Science, DS05 --- Air Quality and Weather Patterns\
**Initial geography:** Bengaluru, Karnataka, India\
**Active builders:** Suprith and Uday\
**Hackathon duration:** 8 hours (confirm event clock and submission
deadline with organizers)

## 1. Mission

Build a real, working, explainable air-quality analytics and short-term
forecasting platform using genuine, traceable environmental data. The
product must help users understand historical air-quality patterns,
relationships with weather, unusual pollution periods, and (only if data
supports it) short-term PM2.5 forecasts.

This is not a static dashboard, fake AI demo, or collection of hardcoded
charts.

## 2. Autonomy and approval

-   The BreatheWise concept and initial plan have been approved by
    Suprith.
-   Organizer permissions reported by the team: AI tools allowed;
    external APIs allowed; datasets allowed; prebuilt code/libraries
    allowed; external development tools allowed.
-   Team size limit is four. Current active builders are Suprith and
    Uday. Two other teammates may explain/present the project; do not
    claim they implemented work they did not do.
-   Before implementation, complete organizer checks and inspect the
    actual dataset. Do not claim those gates are complete until evidence
    is available.
-   Once the data and compliance gates are complete, proceed
    autonomously within this approved scope. Ask only when a decision
    materially changes scope, cost, risk, or organizer compliance.

## 3. Truth and data integrity --- non-negotiable

-   Use genuine observations from documented public sources. Do not
    invent records, measurements, timestamps, labels, statistics,
    charts, forecasts, model scores, or API responses.
-   Never present synthetic/random/demo data as real observations, model
    training data, evaluation data, or evidence.
-   Preserve original raw data. Keep a reproducible cleaning pipeline
    and record transformations.
-   Record source URL, provider, retrieval date, date coverage,
    station/location, units, license/terms, and known limitations.
-   Clearly distinguish measured observations, reanalysis weather data,
    modelled estimates, and forecasts.
-   If an API fails, use a genuine cached copy and display its actual
    last-updated time. Never label cached data as live.
-   Do not combine different stations, sensors, time zones, units, or
    data products without checking compatibility and documenting the
    method.
-   Missing values must remain missing or be handled by a justified
    method. Do not fabricate values to fill gaps.
-   Do not infer causation from correlation or feature importance.

## 4. Scientific and modelling rules

-   Start with exploratory data analysis, not model selection.
-   Choose a target only after inspecting data coverage, sampling
    frequency, missingness, and quality.
-   Preferred first target: future PM2.5 concentration. Predict overall
    AQI only if the required pollutant coverage and official calculation
    requirements are satisfied.
-   Use chronological train/validation/test splits for time-series work.
    Prevent leakage from future values, rolling windows, target-derived
    features, or random shuffling.
-   Compare against a simple baseline (for example, persistence or
    seasonal baseline).
-   Report suitable metrics such as MAE and RMSE, plus test period and
    sample count. Never invent performance.
-   Feature importance explains model behaviour, not causality.
-   Forecasts must show horizon, timestamp, units, and
    uncertainty/limitations where possible.
-   If historical data is inadequate, ship honest analysis and clearly
    labelled external/model forecasts rather than a misleading trained
    prediction.
-   Anomaly detection flags unusual observations; it does not
    automatically prove an event or cause.
-   Health guidance must be cautious, non-diagnostic, and grounded in
    official guidance. Do not provide medical advice.

## 5. Source and AQI rules

-   CPCB methodology must be followed if displaying India's official
    AQI.
-   India's National AQI is based on pollutant sub-indices; the overall
    AQI is not a simple average of pollutant concentrations.
-   Respect pollutant-specific averaging periods and minimum data
    requirements. If these cannot be met, show pollutant concentrations
    and label official AQI as unavailable rather than calculating an
    invalid value.
-   Clearly identify whether AQI values are sourced from CPCB,
    calculated by a verified implementation of the official method, or
    supplied by another model/provider.
-   Cite and attribute data providers in the UI and README.

## 6. Organizer compliance

Before coding, obtain/record the remaining event details: - Submission
format and deadline. - Judging criteria and demo duration. - Whether
public deployment is required or optional. - GitHub/repository
submission requirements. - Any restrictions on data privacy, licensing,
attribution, internet access, or presentation claims. - Team member
registration and contribution declaration rules. The team has reported
permission for AI, APIs, datasets, prebuilt code, and development tools.
Do not assume unconfirmed rules.

## 7. Approved technical direction

Use the simplest stable stack that meets the deadline: - Python, Pandas,
NumPy for processing and analysis. - Scikit-learn for baseline and
candidate ML models when justified. - FastAPI for backend APIs if a
separate backend is useful. - React + TypeScript + Tailwind for the
frontend if the team can integrate it within the time limit. - Plotly or
Recharts for visualizations. - Local CSV/Parquet and SQLite only if
persistence is needed. - Git for checkpoints. Do not add microservices,
Kubernetes, vector databases, agents, Docker, or paid services unless a
demonstrated need exists. If full-stack integration threatens the
deadline, use a simpler working UI (for example Streamlit) rather than
ship a broken architecture.

## 8. Design rules

-   Use Google Stitch: https://stitch.withgoogle.com/
-   Design only the screens users/judges need to see: Overview,
    Explorer, Weather Relationships, Forecast & Explanation, Insights.
-   Keep the design coherent, accessible, responsive, and premium.
-   Stitch is for visual design and screen exploration; Antigravity
    implements and integrates actual functionality.
-   Review generated code before integrating. Never blindly overwrite
    working code.
-   Every visible primary control must work. No dead buttons or fake
    interactions.
-   Include loading, empty, error, and success states.

## 9. Product requirements

The end-to-end workflow must be real: source data → validation/cleaning
→ analysis/features → model or analytical output → API/backend (if used)
→ UI → user-visible result. The UI must identify data source,
observation time, location/station, units, and whether values are
observed or forecast.

## 10. Security and reliability

-   Keep API keys in environment variables; never commit secrets.
-   Provide `.env.example` with variable names and dummy placeholders
    only.
-   Add `.env`, caches containing secrets, and local environment folders
    to `.gitignore`.
-   Validate user inputs and handle API failures.
-   Cache genuine data locally for offline demonstration.
-   Avoid destructive shell commands and protect working code.
-   Commit working milestones to Git.

## 11. Eight-hour execution rules

-   Hours 0--1: organizer checks, data download, inspect
    schema/coverage/quality.
-   Hours 1--2: cleaning, EDA, define target and baseline.
-   Hours 2--4: vertical slice and MVP dashboard.
-   Hours 4--6: forecast/evaluation, explanation, anomaly feature,
    polish.
-   Hour 6: feature freeze.
-   Hours 6--7: integration, offline and error testing.
-   Hours 7--8: slides, demo script, backup recording, rehearsal.
    Prioritize working product, genuine data, honest insight, premium
    UI, then documentation polish. Security, compliance, and
    truthfulness are mandatory throughout.

## 12. Definition of done

-   Runs locally from documented commands.
-   Core demo works offline from cached genuine data.
-   Data sources, dates, station, units, license, and limitations are
    documented.
-   Cleaning and analysis are reproducible.
-   All visible important interactions work.
-   Forecast, if included, has honest time-based evaluation and a
    baseline.
-   No fabricated data or claims.
-   UI distinguishes observations from forecasts and displays
    timestamps.
-   Critical errors are resolved.
-   README, PRD, architecture, design, phase, memory, and pitch notes
    match actual implementation.
-   Team can explain the problem, data, method, limitations, and demo.
