"""
Unit & Integration Tests for Reproducible Data Pipeline
Run with: pytest backend/test_data_pipeline.py
"""

import os
import json
import pytest

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")


@pytest.fixture(scope="module")
def processed_artifacts():
    """Loads all generated processed artifacts for verification."""
    artifacts = {}
    files = [
        "stations_metadata.json",
        "station_daily_summary.json",
        "city_daily_summary.json",
        "retrospective_weather_correlations.json",
        "diurnal_profiles.json",
        "data_transparency_metrics.json"
    ]
    for fname in files:
        fpath = os.path.join(PROCESSED_DIR, fname)
        assert os.path.exists(fpath), f"Missing artifact: {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            artifacts[fname] = json.load(f)
    return artifacts


class TestStationsMetadata:
    """Tests station metadata integrity and active/decommissioned partitioning."""

    def test_station_counts_and_active_status(self, processed_artifacts):
        stations = processed_artifacts["stations_metadata.json"]
        assert len(stations) == 14, f"Expected 14 cataloged stations, found {len(stations)}"
        
        active_stations = [s for s in stations if s["is_active"]]
        inactive_stations = [s for s in stations if not s["is_active"]]
        
        assert len(active_stations) == 13, f"Expected 13 active stations, found {len(active_stations)}"
        assert len(inactive_stations) == 1, f"Expected 1 inactive station, found {len(inactive_stations)}"
        assert inactive_stations[0]["station_id"] == "site_164"
        assert inactive_stations[0]["valid_aqi_days_count"] == 0

    def test_station_coordinates_and_pollutants(self, processed_artifacts):
        stations = processed_artifacts["stations_metadata.json"]
        for st in stations:
            assert st["latitude"] is not None and 12.0 < st["latitude"] < 14.0
            assert st["longitude"] is not None and 77.0 < st["longitude"] < 78.5
            if st["is_active"]:
                assert st["valid_aqi_days_count"] > 400
                assert "PM10" in st["monitored_parameters"]


class TestDataTransparencyLedger:
    """Tests CPCB 16-hour sufficiency filter counts and provenance verification."""

    def test_16hour_sufficiency_counts(self, processed_artifacts):
        transparency = processed_artifacts["data_transparency_metrics.json"]
        metrics = transparency["audit_metrics"]
        
        assert metrics["total_raw_daily_records"] == 50584
        assert metrics["cpcb_16hour_sufficiency_filtered_out"] == 3789
        assert metrics["compliant_daily_records_preserved"] == 46795
        assert metrics["compliant_daily_records_preserved"] + metrics["cpcb_16hour_sufficiency_filtered_out"] == 50584


class TestCityDailySummary:
    """Tests continuous city composite AQI calculation across the 670-day window."""

    def test_date_span_and_continuity(self, processed_artifacts):
        summary = processed_artifacts["city_daily_summary.json"]
        assert len(summary) == 670, f"Expected 670 calendar days, got {len(summary)}"
        assert summary[0]["date"] == "2023-01-01"
        assert summary[-1]["date"] == "2024-10-31"

    def test_aqi_bounds_and_categories(self, processed_artifacts):
        summary = processed_artifacts["city_daily_summary.json"]
        for row in summary:
            aqi = row["city_aqi"]
            assert aqi is not None, f"Missing city AQI on {row['date']}"
            assert 0 <= aqi <= 500, f"City AQI out of bounds ({aqi}) on {row['date']}"
            
            category = row["category"]
            assert category in ("Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe")
            
            # Verify category matches AQI value
            if aqi <= 50:
                assert category == "Good"
            elif aqi <= 100:
                assert category == "Satisfactory"
            elif aqi <= 200:
                assert category == "Moderate"
            elif aqi <= 300:
                assert category == "Poor"
            elif aqi <= 400:
                assert category == "Very Poor"
            else:
                assert category == "Severe"

    def test_weather_variables_presence(self, processed_artifacts):
        summary = processed_artifacts["city_daily_summary.json"]
        for row in summary:
            assert row["temp_mean"] is not None
            assert row["humidity_mean"] is not None
            assert row["pressure_mean"] is not None
            assert row["wind_speed_resultant"] is not None
            assert row["precipitation_sum"] is not None and row["precipitation_sum"] >= 0.0


class TestRetrospectiveWeatherCorrelations:
    """Tests Pearson correlation bounds and atmospheric physical directionality."""

    def test_correlations_bounded_and_physical(self, processed_artifacts):
        corrs = processed_artifacts["retrospective_weather_correlations.json"]
        matrix = corrs["correlation_matrix"]
        
        # Pearson correlations must be strictly within [-1.0, 1.0]
        for p, w_dict in matrix.items():
            for w, val in w_dict.items():
                if val is not None:
                    assert -1.0 <= val <= 1.0, f"Correlation out of bounds: {p} vs {w} = {val}"

        # Physically grounded atmospheric checks:
        # 1. PM2.5 vs Wind Speed must be negative (aerodynamic dispersion)
        pm25_wind = matrix["pm25"]["wind_speed_resultant"]
        assert pm25_wind is not None and pm25_wind < 0.0, f"PM2.5 vs Wind expected negative, got {pm25_wind}"

        # 2. PM10 vs Precipitation must be negative (wet scavenging/washout)
        pm10_rain = matrix["pm10"]["precipitation_sum"]
        assert pm10_rain is not None and pm10_rain < 0.0, f"PM10 vs Rain expected negative, got {pm10_rain}"


class TestLandmarkDiurnalProfiles:
    """Tests descriptive hourly profiles for BTM Layout and Peenya."""

    def test_diurnal_24h_curves(self, processed_artifacts):
        diurnal = processed_artifacts["diurnal_profiles.json"]
        assert "BTM Layout" in diurnal
        assert "Peenya" in diurnal
        
        for st_name in ["BTM Layout", "Peenya"]:
            curves = diurnal[st_name]["diurnal_curves"]
            assert "PM10" in curves
            assert "NO2" in curves
            
            # Check 24 hours present
            for param in ["PM10", "NO2"]:
                param_curve = curves[param]
                assert len(param_curve) == 24
                for pt in param_curve:
                    assert 0 <= pt["hour"] <= 23
                    assert pt["sample_count"] > 0
                    assert pt["mean_concentration"] is not None and pt["mean_concentration"] > 0
