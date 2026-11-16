# BreatheWise --- Team Explanation and Presentation Brief

**Audience:** Two teammates who will explain the project idea,
procedure, and technical approach.\
**Project builders:** Suprith and Uday.\
**Track:** Data Science --- DS05 Air Quality and Weather Patterns.

## 1. Explain the project in one sentence

BreatheWise is a Bengaluru-focused air-quality and weather intelligence
platform that explores real pollution data, studies weather
relationships, detects unusual pollution patterns, and forecasts
short-term PM2.5 only when the data supports a reliable model.

## 2. The problem we are addressing

Air quality changes over time. A single AQI number does not explain: -
Which pollutants are elevated. - How pollution changes across hours,
days or seasons. - Whether pollutant levels are associated with
temperature, humidity, wind or rainfall. - Whether a period is unusual
compared with historical patterns. - What a short-term forecast
suggests, and how uncertain it is.

We are building a tool to explore these questions with real data.

## 3. What the product does

### Explorer

-   Cleans and analyzes environmental data.
-   Displays pollutant trends and summary statistics.
-   Compares pollutant levels across time.
-   Examines associations with weather.

### Innovator

-   Trains and evaluates a PM2.5 forecasting model if the dataset has
    enough valid historical observations.
-   Compares it with a simple baseline.
-   Explains model feature importance.
-   Flags unusual pollution readings.
-   Generates evidence-based, cautious insights.

## 4. What makes it distinctive

**Pollution Pattern Explainer:** It does not merely show a forecast
number. It summarizes the actual recent pollution trend, the pollutant
being examined, weather context, and uncertainty. It must not claim
weather caused a change unless there is evidence beyond correlation.

## 5. Data sources and why we chose them

### Main candidate: CPCB Peenya data

The OpenCity catalogue lists a Peenya CPCB 15-minute 2024--25 CSV
resource. Metadata includes timestamps, pollutants, and weather-related
columns such as temperature, relative humidity, wind, rainfall and
pressure.

Link:
https://data.opencity.in/dataset/bengaluru-hourly-air-quality-reports/resource/c6b4282e-43c8-4f14-a855-83e4b52a80d7

Important: metadata has been inspected, but the actual CSV still needs
to be downloaded and validated. Do not say we have completed the data
analysis or model training.

### Alternative: OpenAQ Jayanagar station

OpenAQ lists Jayanagar 5th Block, Bengaluru --- KSPCB, reporting since
2018. We may use it as an alternative or supplementary source after
checking the actual measurements and coverage.

https://explore.openaq.org/locations/6973

### Weather: Open-Meteo

Historical weather reanalysis can supplement weather fields if needed.
It is not identical to a local station sensor reading and needs
attribution.

https://open-meteo.com/en/docs/historical-weather-api

## 6. Technical workflow

Explain this sequence:

1.  **Data collection:** Download public air-quality and weather data.
2.  **Data inspection:** Check columns, timestamps, units, date range
    and station.
3.  **Data cleaning:** Handle missing, duplicate, invalid and irregular
    records transparently.
4.  **Exploratory analysis:** Calculate summary statistics and visualize
    time trends.
5.  **Weather relationship analysis:** Align weather and pollution by
    time/location; inspect correlations and patterns.
6.  **Feature engineering:** Create past-only lag and rolling features
    for forecasting.
7.  **Model development:** Compare a simple baseline with an ML model.
8.  **Evaluation:** Use chronological test data and report actual
    MAE/RMSE.
9.  **Explanation:** Show feature importance and anomalies with
    limitations.
10. **Dashboard:** Connect the actual analysis to an interactive
    interface.
11. **Offline demo:** Cache genuine data and model assets locally.

## 7. Roles

-   **Suprith:** Product and integration lead; frontend, backend
    integration, dashboard, end-to-end testing and presentation.
-   **Uday:** Data Science lead; dataset collection, cleaning, EDA,
    model training and evaluation.
-   **Two explaining/presentation teammates:** Learn the problem, data
    sources, pipeline, model evaluation, product screens, limitations
    and demo sequence. Describe their actual contribution accurately.

All team members should understand the end-to-end flow.

## 8. Suggested speaking split

### Speaker 1 --- Problem and solution (about 45 seconds)

"Air quality is often presented as a single number, but that number does
not explain the pollutant trends, weather relationships or unusual
changes. BreatheWise is our DS05 solution: an interactive platform to
explore real air-quality and weather data and understand pollution
patterns."

### Speaker 2 --- Data and procedure (about 60 seconds)

"We are using public monitoring data, with Bengaluru CPCB station data
as our first candidate and OpenAQ as an alternative. We inspect and
clean timestamps, units, missing values and station coverage before
analysis. We then perform exploratory analysis and align weather
information with pollution observations."

### Speaker 1 or 2 --- Innovation and model (about 45 seconds)

"Our innovation is the Pollution Pattern Explainer. If the historical
data is suitable, we forecast PM2.5, compare the model against a simple
baseline on unseen future dates, and explain which features influence
its predictions. We also identify unusual readings. We do not claim
correlation proves causation."

### Final speaker --- Demo and impact (about 30 seconds)

"The dashboard makes the analysis accessible through trends, weather
relationships, anomalies and, when validated, forecasts. It is designed
to run locally using cached genuine data so the demo does not depend on
internet availability."

Do not use this script as a claim that features are already implemented.
Update the tense after actual development.

## 9. Likely judge questions

**Q: Why Bengaluru?**\
A: It gives us a focused local study area and there are public
monitoring-station data resources to investigate.

**Q: Why PM2.5 forecasting?**\
A: It is our initial candidate target. We will only include a trained
forecast if historical coverage and time-based evaluation support it.

**Q: How do you know the model works?**\
A: We compare it with a simple baseline on a chronological held-out test
period and report actual MAE/RMSE. We do not invent accuracy.

**Q: Does weather cause pollution?**\
A: Our correlation analysis only identifies associations. It does not
establish causation.

**Q: Is your AQI official?**\
A: We only label it official if we implement CPCB methodology and
satisfy the required pollutant averaging and data completeness rules.
Otherwise, we show pollutant concentrations separately.

**Q: What if the API or internet is down?**\
A: We use locally cached genuine data and display the actual timestamp
of the cached observations.

**Q: What are the limitations?**\
A: A monitoring station may not represent the whole city; data can have
missing or invalid readings; reanalysis weather is not a local sensor;
and forecasts are uncertain.

## 10. What not to say

-   Do not say "100% accurate."
-   Do not invent model accuracy or number of records.
-   Do not claim all Bengaluru air quality from one station.
-   Do not say weather caused pollution based on correlation.
-   Do not call modelled/reanalysis data direct sensor measurements.
-   Do not claim the model or dashboard is complete before it works.
-   Do not claim all four members coded the project if only two built
    it.

## 11. Team preparation checklist

-   [ ] Both presenters can explain the problem without reading.
-   [ ] Both can explain where the data comes from.
-   [ ] Both understand the cleaning and analysis steps.
-   [ ] Both understand the difference between observed data and
    forecasts.
-   [ ] Both can explain train/test time split and baseline.
-   [ ] Both know the real model metrics once available.
-   [ ] Both know current limitations.
-   [ ] Both can run through the demo.
