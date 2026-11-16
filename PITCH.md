# BreatheWise --- Pitch and Demo Notes

## One-line pitch

BreatheWise turns real air-quality and weather observations into
understandable pollution trends, weather relationships, unusual-event
flags, and explainable short-term PM2.5 forecasts when supported by
data.

## Problem

People may see an air-quality number but cannot easily explore how
pollutant levels change over time, how they relate to weather, or what
recent patterns suggest about the near future.

## Solution

A data-driven dashboard for: 1. Historical pollutant exploration. 2.
Weather relationship analysis. 3. Unusual pollution-period detection. 4.
Explainable PM2.5 forecasting, if validated. 5. Evidence-based, cautious
insights.

## Why it is different

The distinctive feature is the Pollution Pattern Explainer. Instead of
displaying only a chart or forecast number, it summarizes the actual
recent trend, relevant weather observations, pollutant context, and
forecast uncertainty. It must not claim causation.

## Data story

Primary candidate: Bengaluru CPCB Peenya 15-minute 2024--25 dataset
listed by OpenCity. Alternative: OpenAQ Jayanagar 5th Block historical
station. Weather supplement: Open-Meteo historical reanalysis if needed.
Final dataset must be named only after actual file inspection and
validation.

## Technical story

Raw data → validation/cleaning → time/location alignment → EDA → feature
engineering → baseline/model evaluation → API/service → dashboard.

## Demo sequence (adapt to implemented product)

1.  Open Overview and identify selected station, source and last
    observation timestamp.
2.  Open Explorer; select PM2.5 and a date range; explain a real
    pattern.
3.  Open Weather Relationships; show an actual association and explain
    correlation is not causation.
4.  Open Insights; demonstrate an anomaly with its detection method.
5.  Open Forecast only if the model passed held-out time-based
    evaluation; explain baseline, MAE/RMSE, horizon and uncertainty.
6.  Demonstrate offline operation using cached data.

## Suggested 2--3 minute presentation

-   0:00--0:25 --- Problem and why it matters.
-   0:25--0:50 --- BreatheWise solution and target users.
-   0:50--1:20 --- Real data sources and cleaning.
-   1:20--1:50 --- Analysis and modelling method.
-   1:50--2:30 --- Live product demo.
-   2:30--2:50 --- Results, limitations and next steps.

## Judge questions to prepare

**Why Bengaluru?** It gives the project a focused local scope and allows
investigation of available local monitoring stations.

**Why PM2.5?** It is a commonly monitored pollutant and a suitable
initial forecasting target, subject to data quality and coverage.

**How do you know the model works?** We use chronological held-out
evaluation and compare against a simple baseline. We report actual
metrics and test dates.

**Can weather cause pollution?** Weather can be associated with
pollutant concentration and dispersion, but correlation in our analysis
does not prove causation.

**Is this official AQI?** Only if we implement CPCB methodology and
satisfy pollutant-specific averaging and data completeness requirements.
Otherwise, we show pollutant concentrations and label AQI unavailable.

**What if the API fails?** Core demo uses genuine cached data and
clearly shows its last-updated timestamp.

**What are limitations?** Station coverage may not represent the entire
city; sensors can have missing/invalid readings; weather reanalysis
differs from local measurements; forecasts are uncertain.

## Presentation honesty

Do not claim a feature is built until it works. Do not quote invented
metrics, sample sizes, coverage, accuracy, user impact or deployment
status. Update this file after implementation with actual results and
screenshots.
