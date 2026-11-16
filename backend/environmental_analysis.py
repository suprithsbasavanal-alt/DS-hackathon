"""
BreatheWise - Environmental Analysis & Pattern Aggregation Engine
Computes retrospective correlation matrices, orthogonal wind vectors, and unified multi-pollutant summaries.
"""

import os
import json
import math
from typing import Dict, List, Optional, Tuple, Any
from fastapi import HTTPException
from scipy.stats import pearsonr, spearmanr

from backend.schemas.environmental import (
    StationMetadataItem,
    AQISummaryItem,
    PollutantStatusItem,
    MeteorologyContextItem,
    CorrelationItem,
    EnvironmentalInsightsResponse,
)
from backend.threshold_engine import evaluate_all_criteria_pollutants

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

_DATA_CACHE: Dict[str, Any] = {}
_CORRELATION_CACHE: Optional[List[CorrelationItem]] = None


def _load_json(filename: str) -> Any:
    if filename not in _DATA_CACHE:
        fpath = os.path.join(PROCESSED_DIR, filename)
        if not os.path.exists(fpath):
            raise FileNotFoundError(f"Processed artifact not found: {filename}")
        with open(fpath, "r", encoding="utf-8") as f:
            _DATA_CACHE[filename] = json.load(f)
    return _DATA_CACHE[filename]


def compute_wind_components(
    wind_speed: Optional[float],
    wind_dir: Optional[float]
) -> Tuple[Optional[float], Optional[float]]:
    """
    Computes orthogonal zonal (u) and meridional (v) wind velocity components from speed and direction.
    - u: Zonal velocity (positive = eastward, westerly wind)
    - v: Meridional velocity (positive = northward, southerly wind)
    Direction convention: Wind direction theta in degrees clockwise from North (direction wind blows from).
    """
    if wind_speed is None or wind_dir is None:
        return None, None
    try:
        ws = float(wind_speed)
        wd = float(wind_dir)
        rad = math.radians(wd)
        u = round(-ws * math.sin(rad), 2)
        v = round(-ws * math.cos(rad), 2)
        return u, v
    except (ValueError, TypeError):
        return None, None


def compute_retrospective_correlations(station_id: str = "city_composite") -> List[CorrelationItem]:
    """
    Computes Pearson r and Spearman rho correlations across the 670 daily city composite records.
    Every item includes the exact sample size (N=670), explicit scope ('citywide_historical'),
    a scope note explaining context, and descriptive non-causal phrasing.
    """
    city_data = _load_json("city_daily_summary.json")

    records = []
    for r in city_data:
        ws = r.get("wind_speed_resultant")
        wd = r.get("wind_dir_resultant")
        u, v = compute_wind_components(ws, wd)
        records.append({
            "city_aqi": r.get("city_aqi"),
            "pm25": r.get("pm25"),
            "pm10": r.get("pm10"),
            "no2": r.get("no2"),
            "temp_mean": r.get("temp_mean"),
            "humidity_mean": r.get("humidity_mean"),
            "wind_speed_resultant": ws,
            "wind_u": u,
            "wind_v": v,
            "precipitation_sum": r.get("precipitation_sum"),
            "pressure_mean": r.get("pressure_mean"),
        })

    pair_configs = [
        (
            "pressure_mean", "city_aqi",
            "Higher surface pressure was historically associated with higher city AQI in this dataset (r = +0.607). Observational co-occurrence only; does not prove an atmospheric trapping mechanism."
        ),
        (
            "humidity_mean", "city_aqi",
            "Relative humidity exhibited a negative linear correlation with city AQI (r = -0.623), reflecting monsoon washout during high-humidity months."
        ),
        (
            "wind_speed_resultant", "city_aqi",
            "Higher surface wind speed was moderately associated with lower AQI (r = -0.284), consistent with aerodynamic dispersion."
        ),
        (
            "precipitation_sum", "city_aqi",
            "Daily precipitation exhibited an inverse association with city AQI (r = -0.419), reflecting wet scavenging of particulate matter."
        ),
        (
            "wind_u", "city_aqi",
            "Zonal wind velocity u was negatively associated with city AQI (r = -0.631); positive u (westerlies during monsoon) corresponds to cleaner background air."
        ),
        (
            "wind_v", "city_aqi",
            "Meridional wind velocity v exhibited weak association with city AQI (r = -0.141)."
        ),
        (
            "temp_mean", "city_aqi",
            "Mean daily temperature exhibited weak direct linear correlation with composite city AQI (r = +0.105)."
        ),
        (
            "pm25", "city_aqi",
            "Fine particulate PM2.5 exhibited strong positive association with city AQI (r = +0.896) as a primary criteria driver."
        ),
        (
            "pm10", "city_aqi",
            "Coarse particulate PM10 exhibited strong positive association with city AQI (r = +0.956) as the dominant prominent pollutant."
        ),
        (
            "no2", "city_aqi",
            "Nitrogen dioxide NO2 exhibited moderate positive association with city AQI (r = +0.465), reflecting combustion and vehicular traffic patterns."
        ),
    ]

    scope_note = (
        "Computed across 670 Bengaluru city composite daily records (Jan 2023–Oct 2024)."
        if station_id == "city_composite"
        else f"Citywide historical baseline (N=670). Provided for regional atmospheric context; not isolated to station '{station_id}'."
    )

    correlation_items = []
    for var_x, var_y, desc in pair_configs:
        xs = []
        ys = []
        for row in records:
            vx = row.get(var_x)
            vy = row.get(var_y)
            if vx is not None and vy is not None:
                xs.append(float(vx))
                ys.append(float(vy))

        n_samples = len(xs)
        if n_samples < 3:
            continue

        p_r, p_val = pearsonr(xs, ys)
        s_rho, s_val = spearmanr(xs, ys)

        correlation_items.append(
            CorrelationItem(
                metric_x=var_x,
                metric_y=var_y,
                pearson_r=round(float(p_r), 3),
                spearman_rho=round(float(s_rho), 3),
                n_samples=n_samples,
                p_value=float(p_val) if not math.isnan(p_val) else None,
                scope="citywide_historical",
                scope_note=scope_note,
                description=desc
            )
        )

    return correlation_items


def get_environmental_insights(
    station_id: str = "city_composite",
    date_str: str = "2024-10-31"
) -> EnvironmentalInsightsResponse:
    """
    Builds the complete EnvironmentalInsightsResponse for a specific station and date.
    Performs full input validation and enforces CPCB regulatory and transparency boundaries.
    """
    stations_meta = _load_json("stations_metadata.json")
    all_station_ids = [s["station_id"] for s in stations_meta]

    # 1. Station ID Validation
    if station_id != "city_composite" and station_id not in all_station_ids:
        raise HTTPException(status_code=404, detail=f"Station '{station_id}' not found.")

    # 2. Decommissioned Station Handling (site_164)
    # Omits correlations to eliminate risk of users confusing citywide statistics with station data.
    if station_id == "site_164":
        st_meta = next(s for s in stations_meta if s["station_id"] == "site_164")
        station_item = StationMetadataItem(
            id="site_164",
            name=st_meta["station_name"],
            active_stations_count=0,
            latitude=st_meta["latitude"],
            longitude=st_meta["longitude"],
            is_active=False,
            status="decommissioned",
            message="Station decommissioned August 2022. No observations in active 2023–2024 dataset."
        )
        return EnvironmentalInsightsResponse(
            status="success",
            date=date_str,
            is_historical=True,
            station=station_item,
            aqi_summary=AQISummaryItem(
                aqi=None,
                category="Decommissioned",
                prominent_pollutant=None,
                category_meta={
                    "name": "Decommissioned",
                    "color": "#94A3B8",
                    "badge": "bg-slate-500/10 text-slate-500 border-slate-500/20",
                    "desc": "Station decommissioned in August 2022. No observations available."
                }
            ),
            pollutants=[],
            meteorology=MeteorologyContextItem(),
            correlation_scope="omitted",
            correlations=[],
            data_integrity={
                "is_decommissioned": True,
                "correlations_omitted": True,
                "message": "Station decommissioned August 2022. Correlations omitted to avoid conflating citywide statistics with station data."
            }
        )

    # 3. Locate Target Record
    target_record: Optional[Dict[str, Any]] = None
    station_meta_dict: Optional[Dict[str, Any]] = None

    if station_id == "city_composite":
        city_data = _load_json("city_daily_summary.json")
        target_record = next((r for r in city_data if r.get("date") == date_str), None)
        station_item = StationMetadataItem(
            id="city_composite",
            name="Bengaluru City Composite",
            active_stations_count=target_record.get("reporting_stations_count", 13) if target_record else 13,
            is_active=True,
            status="active"
        )
    else:
        st_meta = next(s for s in stations_meta if s["station_id"] == station_id)
        station_daily = _load_json("station_daily_summary.json")
        daily_records = station_daily.get(station_id, [])
        target_record = next((r for r in daily_records if r.get("date") == date_str), None)
        station_item = StationMetadataItem(
            id=st_meta["station_id"],
            name=st_meta["station_name"],
            latitude=st_meta["latitude"],
            longitude=st_meta["longitude"],
            is_active=st_meta["is_active"],
            status="active" if st_meta["is_active"] else "inactive"
        )

    # 4. Date Validation
    if not target_record:
        raise HTTPException(
            status_code=404,
            detail=f"No data available for date: '{date_str}' at station '{station_id}'."
        )

    # 5. Build Pollutant Assessment
    pollutant_data = {
        "pm25": target_record.get("pm25"),
        "pm10": target_record.get("pm10"),
        "no2": target_record.get("no2"),
        "so2": target_record.get("so2"),
        "co": target_record.get("co"),
        "o3": target_record.get("o3"),
        "nh3": target_record.get("nh3"),
        "pb": None,  # Explicitly unmonitored
    }
    evaluated_pollutants = evaluate_all_criteria_pollutants(pollutant_data, is_daily=True)

    # 6. Build AQI Summary
    aqi_summary = AQISummaryItem(
        aqi=target_record.get("city_aqi") if station_id == "city_composite" else target_record.get("aqi"),
        category=target_record.get("category", "Unknown"),
        prominent_pollutant=target_record.get("prominent_pollutant"),
        category_meta=target_record.get("category_meta")
    )

    # 7. Build Meteorology Context
    ws = target_record.get("wind_speed_resultant")
    wd = target_record.get("wind_dir_resultant")
    u, v = compute_wind_components(ws, wd)

    meteorology = MeteorologyContextItem(
        temperature_mean=target_record.get("temp_mean"),
        temp_min=target_record.get("temp_min"),
        temp_max=target_record.get("temp_max"),
        humidity_mean=target_record.get("humidity_mean"),
        wind_speed_resultant=ws,
        wind_dir_resultant=wd,
        wind_u=u,
        wind_v=v,
        precipitation_sum=target_record.get("precipitation_sum"),
        pressure_mean=target_record.get("pressure_mean"),
    )

    # 8. Retrospective Correlations with Scope Demarcation
    correlations = compute_retrospective_correlations(station_id=station_id)

    return EnvironmentalInsightsResponse(
        status="success",
        date=date_str,
        is_historical=True,
        station=station_item,
        aqi_summary=aqi_summary,
        pollutants=evaluated_pollutants,
        meteorology=meteorology,
        correlation_scope="citywide_historical",
        correlations=correlations,
        data_integrity={
            "reporting_stations_count": target_record.get("reporting_stations_count"),
            "data_source": "CPCB/CAAQM & ERA5 Reanalysis",
            "n_historical_days": 670,
            "correlation_context": "Citywide historical composite (N=670)"
        }
    )
