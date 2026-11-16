"""
BreatheWise - Fast, Offline-Ready FastAPI Backend
Serves verified CPCB air quality and ERA5 reanalysis data,
retrospective meteorological analytics, autoregressive forecasting benchmarks,
and data-transparency ledgers.
"""

import os
import json
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
FRONTEND_DIST = os.path.join(BASE_DIR, "frontend", "dist")

app = FastAPI(
    title="BreatheWise Bengaluru Air Quality & Weather API",
    description="Offline-first Data Science API for Bengaluru Air Quality & Meteorology",
    version="1.2.0"
)

# Enable CORS for local Vite dev server and offline localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-Memory Cache for fast, zero-latency offline response
_CACHE: Dict[str, Any] = {}


def get_cached_json(filename: str) -> Any:
    """Loads and caches processed JSON data artifacts."""
    if filename not in _CACHE:
        fpath = os.path.join(PROCESSED_DIR, filename)
        if not os.path.exists(fpath):
            raise HTTPException(status_code=500, detail=f"Processed artifact not found: {filename}")
        with open(fpath, "r", encoding="utf-8") as f:
            _CACHE[filename] = json.load(f)
    return _CACHE[filename]


@app.get("/api/health")
def health_check() -> Dict[str, Any]:
    """Health check endpoint confirming offline-ready status."""
    city_data = get_cached_json("city_daily_summary.json")
    return {
        "status": "healthy",
        "service": "BreatheWise Air Quality & Meteorology Engine",
        "version": "1.2.0",
        "city": "Bengaluru, Karnataka, India",
        "offline_ready": True,
        "total_historical_days": len(city_data),
        "data_range": f"{city_data[0]['date']} to {city_data[-1]['date']}"
    }


@app.get("/api/city/summary")
def get_city_summary() -> Dict[str, Any]:
    """
    Returns latest historical city composite AQI, category, prominent pollutant,
    active station count, realized weather, and a 14-day recent sparkline.
    """
    city_data = get_cached_json("city_daily_summary.json")
    if not city_data:
        raise HTTPException(status_code=404, detail="City summary data empty.")

    latest = city_data[-1]
    sparkline = [
        {"date": r["date"], "city_aqi": r["city_aqi"], "category": r["category"]}
        for r in city_data[-14:]
    ]

    return {
        "city": "Bengaluru",
        "latest_date": latest["date"],
        "city_aqi": latest["city_aqi"],
        "category": latest["category"],
        "category_meta": latest["category_meta"],
        "prominent_pollutant": latest["prominent_pollutant"],
        "reporting_stations_count": latest["reporting_stations_count"],
        "concentrations": {
            "PM2.5": latest.get("pm25"),
            "PM10": latest.get("pm10"),
            "NO2": latest.get("no2"),
            "SO2": latest.get("so2"),
            "CO": latest.get("co"),
            "Ozone": latest.get("o3"),
            "NH3": latest.get("nh3"),
        },
        "weather": {
            "temp_mean": latest.get("temp_mean"),
            "temp_min": latest.get("temp_min"),
            "temp_max": latest.get("temp_max"),
            "humidity_mean": latest.get("humidity_mean"),
            "precipitation_sum": latest.get("precipitation_sum"),
            "wind_speed_resultant": latest.get("wind_speed_resultant"),
            "wind_dir_resultant": latest.get("wind_dir_resultant"),
            "pressure_mean": latest.get("pressure_mean"),
        },
        "sparkline_14d": sparkline
    }


@app.get("/api/stations")
def get_stations() -> List[Dict[str, Any]]:
    """Returns all 14 monitoring stations with coordinates, active status, and latest AQI."""
    stations = get_cached_json("stations_metadata.json")
    station_daily = get_cached_json("station_daily_summary.json")

    results = []
    for st in stations:
        st_id = st["station_id"]
        daily_records = station_daily.get(st_id, [])
        latest_record = daily_records[-1] if daily_records else None

        st_info = dict(st)
        if latest_record and st["is_active"]:
            st_info["latest_aqi"] = latest_record.get("aqi")
            st_info["latest_category"] = latest_record.get("category")
            st_info["latest_category_meta"] = latest_record.get("category_meta")
            st_info["latest_prominent"] = latest_record.get("prominent_pollutant")
            st_info["latest_date"] = latest_record.get("date")
        else:
            st_info["latest_aqi"] = None
            st_info["latest_category"] = "Decommissioned" if not st["is_active"] else "No Data"
            st_info["latest_category_meta"] = {
                "name": st_info["latest_category"],
                "color": "#94A3B8",
                "badge": "bg-slate-500/10 text-slate-500 border-slate-500/20",
                "desc": "Station decommissioned in August 2022." if not st["is_active"] else "Insufficient data."
            }
            st_info["latest_prominent"] = None
            st_info["latest_date"] = None

        results.append(st_info)

    return results


@app.get("/api/stations/{station_id}/summary")
def get_station_summary(station_id: str) -> Dict[str, Any]:
    """Returns historical daily records and metadata for a specific station."""
    stations = get_cached_json("stations_metadata.json")
    st_meta = next((s for s in stations if s["station_id"] == station_id), None)
    if not st_meta:
        raise HTTPException(status_code=404, detail=f"Station not found: {station_id}")

    station_daily = get_cached_json("station_daily_summary.json")
    records = station_daily.get(station_id, [])

    return {
        "metadata": st_meta,
        "total_records": len(records),
        "history": records[-60:] if records else []  # Latest 60 days
    }


@app.get("/api/analytics/trends")
def get_analytics_trends(
    start_date: Optional[str] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date YYYY-MM-DD")
) -> List[Dict[str, Any]]:
    """Returns continuous daily city composite time series with weather features."""
    city_data = get_cached_json("city_daily_summary.json")
    filtered = city_data

    if start_date:
        filtered = [r for r in filtered if r["date"] >= start_date]
    if end_date:
        filtered = [r for r in filtered if r["date"] <= end_date]

    return filtered


@app.get("/api/analytics/weather-impact")
def get_weather_impact() -> Dict[str, Any]:
    """Returns retrospective Pearson correlation matrix and atmospheric insights."""
    return get_cached_json("retrospective_weather_correlations.json")


@app.get("/api/analytics/diurnal")
def get_diurnal_profiles() -> Dict[str, Any]:
    """Returns descriptive 24-hour diurnal profiles for landmark stations BTM and Peenya."""
    return get_cached_json("diurnal_profiles.json")


@app.get("/api/forecast/backtest")
def get_forecast_backtest() -> Dict[str, Any]:
    """Returns autoregressive ML model evaluation vs Persistence baseline."""
    return get_cached_json("model_evaluation.json")


@app.get("/api/transparency")
def get_data_transparency() -> Dict[str, Any]:
    """Returns CPCB 16-hour sufficiency audit counts, data provenance, and compliance ledger."""
    return get_cached_json("data_transparency_metrics.json")


# ---------------------------------------------------------
# Phase B: Environmental Intelligence & Threshold Foundation
# ---------------------------------------------------------
from backend.schemas.environmental import EnvironmentalInsightsResponse
from backend.environmental_analysis import get_environmental_insights


@app.get("/api/ai/insights", response_model=EnvironmentalInsightsResponse)
def get_ai_insights(
    station_id: str = Query("city_composite", description="Station ID or 'city_composite'"),
    date: str = Query("2024-10-31", description="Observation date (YYYY-MM-DD)")
) -> EnvironmentalInsightsResponse:
    """
    Returns multi-pollutant threshold assessments against CPCB Table 3.2,
    orthogonal wind components (u, v), meteorological context, and retrospective correlation matrices.
    """
    return get_environmental_insights(station_id=station_id, date_str=date)


# ---------------------------------------------------------
# Phase C: Exploratory Environmental Regimes
# ---------------------------------------------------------
from backend.schemas.regimes import EnvironmentalRegimesResponse
from backend.environmental_regimes import get_environmental_regimes


@app.get("/api/ai/regimes", response_model=EnvironmentalRegimesResponse)
def get_ai_regimes(
    force_fallback: bool = Query(False, description="Force deterministic seasonal quantile fallback for testing/degradation")
) -> EnvironmentalRegimesResponse:
    """
    Returns unsupervised standardized k-Means exploratory environmental regimes (d=8)
    with silhouette diagnostic metrics, acceptance heuristic verification, and automated quantile fallback.
    """
    return get_environmental_regimes(force_fallback=force_fallback)


# ---------------------------------------------------------
# Phase D: Decision Support & Physics Simulation
# ---------------------------------------------------------
from backend.schemas.health import HealthAdvisoryResponse
from backend.schemas.purification import (
    PurificationSimulationRequest,
    PurificationSimulationResponse,
)
from backend.health_advisor import evaluate_health_advisories
from backend.purification_simulator import simulate_purification


@app.get("/api/ai/health-advisory", response_model=HealthAdvisoryResponse)
def get_ai_health_advisory(
    aqi: Optional[float] = Query(None, description="Hypothetical custom AQI (0 to 500)"),
    station_id: str = Query("city_composite", description="Station ID or 'city_composite'"),
    date: str = Query("2024-10-31", description="Observation date (YYYY-MM-DD)")
) -> HealthAdvisoryResponse:
    """
    Returns deterministic CPCB-based health guidance with rule IDs, trigger evidence,
    and sensitive cohort advice. Supports both historical observation evaluation and hypothetical queries.
    """
    if aqi is not None:
        return evaluate_health_advisories(
            aqi=aqi,
            pollutants=None,
            evaluation_date=None,
            station_id=None,
            prominent_pollutant=None,
            is_hypothetical=True
        )

    insights = get_environmental_insights(station_id=station_id, date_str=date)
    pollutants_map = {p.name: p.concentration for p in insights.pollutants}
    target_aqi = float(insights.aqi_summary.aqi) if insights.aqi_summary.aqi is not None else 100.0

    return evaluate_health_advisories(
        aqi=target_aqi,
        pollutants=pollutants_map,
        evaluation_date=date,
        station_id=station_id,
        prominent_pollutant=insights.aqi_summary.prominent_pollutant,
        is_hypothetical=False
    )


@app.post("/api/purification/simulate", response_model=PurificationSimulationResponse)
def run_purification_simulation(
    req: PurificationSimulationRequest
) -> PurificationSimulationResponse:
    """
    Executes idealized first-order room CADR decay simulation: C(t) = C0 * exp(-(CADR/V)*t).
    Generates a 40-point decay curve and discloses all 5 physical idealizing assumptions.
    """
    return simulate_purification(
        room_area_m2=req.room_area_m2,
        ceiling_height_m=req.ceiling_height_m,
        initial_pm25_ug_m3=req.initial_pm25_ug_m3,
        cadr_m3_h=req.cadr_m3_h,
        runtime_hours=req.runtime_hours
    )


# Mount static frontend build if it exists (for single-command offline demo)
if os.path.exists(FRONTEND_DIST):
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
