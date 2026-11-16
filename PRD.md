# BreatheWise --- Product Requirements Document (PRD)

**Version:** 0.1 --- Pre-implementation proposal\
**Track:** DS05 --- Air Quality and Weather Patterns\
**Initial study area:** Bengaluru, India

## 1. Product summary

BreatheWise is an air-quality intelligence platform that analyzes public
air-quality and weather observations. It helps users explore pollution
patterns, examine relationships between pollutants and weather, identify
unusual periods, and view short-term PM2.5 forecasts when historical
data supports a valid model.

## 2. Problem statement

Air pollution varies over time and across locations. Users may see an
AQI value but lack an accessible way to investigate historical pollutant
behaviour, seasonal patterns, weather relationships, and likely
near-term changes. The project will turn documented environmental
observations into understandable visual analysis and, where justified,
explainable forecasting.

## 3. Target users

-   Students and educators exploring environmental data.
-   Residents seeking an understandable view of local air-quality
    patterns.
-   Researchers or analysts exploring pollutant and weather
    relationships.
-   Hackathon judges evaluating a practical Data Science application.

The product is an educational/analytical tool, not a medical or
regulatory decision system.

## 4. Goals

1.  Provide transparent exploration of real air-quality data.
2.  Reveal time-based and pollutant-specific patterns.
3.  Analyze associations between weather variables and pollutant levels.
4.  Detect statistically unusual pollution observations.
5.  Build and evaluate a short-term PM2.5 forecasting model if data is
    adequate.
6.  Explain outputs and communicate uncertainty and limitations.

## 5. Non-goals

-   Guaranteeing future air quality.
-   Diagnosing health conditions or prescribing medical action.
-   Claiming pollution causes based only on correlation.
-   Replacing CPCB monitoring or official advisories.
-   Claiming city-wide conditions from one station.
-   Producing an official AQI unless the official CPCB method and data
    requirements are met.
-   Multi-city coverage as a must-have for the first release.

## 6. Core user journey

1.  User opens Overview and sees the selected station, latest available
    observation, pollutant values, source, and timestamp.
2.  User opens Explorer, selects a pollutant and time range, and sees an
    interactive trend.
3.  User compares pollutant behaviour by hour/day/month where coverage
    permits.
4.  User opens Weather Relationships and explores associations with
    temperature, humidity, rainfall, and wind.
5.  User opens Forecast and sees a forecast only if the trained model
    passes evaluation; the horizon and uncertainty are visible.
6.  User opens Insights and reviews unusual periods with evidence and
    cautious interpretation.

## 7. Functional requirements

### FR-01 Data provenance

Display data provider, station/location, date coverage, last update,
units, and observed/modelled/forecast status.

### FR-02 Data quality

Provide a data-quality summary including row count, date range,
missingness, duplicates, invalid values, and sampling intervals.

### FR-03 Historical exploration

Allow pollutant selection and date filtering. Show time-series charts
with units and clear labels.

### FR-04 Summary statistics

Show valid count, mean, median, min, max, and appropriate percentiles.
State the aggregation interval.

### FR-05 Weather analysis

Show pollutant/weather relationships using scatter plots, correlation
values, and time-aligned charts where possible. Explicitly state
correlation is not causation.

### FR-06 Anomaly detection

Flag unusual values or periods using a documented method and threshold.
Provide the observed value, reference window, and method. Do not label
anomalies as confirmed pollution events.

### FR-07 Forecast

Predict future PM2.5 only if the data has sufficient continuity and
quality. Display model, forecast horizon, issue time, units, and
evaluation metrics. Compare with a naive baseline.

### FR-08 Explanation

Show model feature importance or another valid explanation. Explain that
importance is not causation.

### FR-09 Offline use

Core exploration and cached forecast must work without network access
after data/model assets are prepared.

### FR-10 Error states

Handle no data, missing fields, API timeout, invalid date range, and
model unavailable states.

## 8. Data requirements

Candidate sources: - Bengaluru CPCB station CSV resources listed in the
OpenCity Bengaluru Hourly Air Quality Reports dataset catalogue. -
OpenAQ station/sensor measurements as an alternative or supplementary
source. - Open-Meteo historical weather reanalysis if additional weather
variables are needed.

Preferred initial candidate: Peenya CPCB 15-minute 2024--25 CSV. This is
a candidate, not yet an accepted dataset. Its metadata lists fields
including station ID, state, city, station, timestamp, PM2.5, PM10, NO2,
SO2, CO, ozone, temperature, relative humidity, wind speed/direction,
rainfall, solar radiation, and pressure. Some fields are typed as text
and require inspection and numeric conversion checks.

Before acceptance, inspect the actual file and record: - Actual row
count and date range. - Actual column names and units. - Missingness and
invalid values. - Duplicate timestamps and sampling intervals. - Station
identity and time zone. - Whether the dataset contains sufficient
continuity for the proposed forecast target. - Licence and attribution.

## 9. Analytical and ML requirements

-   EDA first.
-   Use PM2.5 as the initial candidate target.
-   Construct lag, rolling, calendar, and weather features only from
    information available at forecast time.
-   Use chronological splits.
-   Compare persistence/seasonal baseline with at least one candidate ML
    model.
-   Evaluate MAE and RMSE on a held-out time period.
-   Do not use future weather observations as model inputs for a
    forecast unless they are genuinely available forecasts at prediction
    time.
-   Explain model limitations and potential distribution shifts.

## 10. Acceptance criteria

-   User can open the dashboard and identify the selected station and
    latest cached observation.
-   User can select a pollutant and inspect a labelled historical chart.
-   User can inspect summary statistics and data quality.
-   User can explore at least one pollutant/weather relationship based
    on aligned data.
-   Anomaly flags, if shown, are reproducible and method-labelled.
-   Forecast, if shown, is generated by a saved model and evaluated
    chronologically against a baseline.
-   If forecast quality/data is inadequate, the product clearly says
    forecasting is unavailable or limited.
-   Source and timestamp are visible.
-   Main workflow works offline from cached files.
-   No important visible control is inert.

## 11. Success measures

Product success is measured by successful end-to-end demonstration, data
provenance, reproducible analysis, honest evaluation, understandable
insights, and stable offline operation---not by an invented accuracy
target.

## 12. Open decisions

-   Final dataset and station: pending actual file inspection.
-   Final forecast horizon: pending sampling continuity and evaluation.
-   Whether to show official AQI: only after CPCB method/data
    sufficiency check.
-   Final frontend architecture: confirm team speed after vertical
    slice.
-   Submission requirements: confirm with organizers.
