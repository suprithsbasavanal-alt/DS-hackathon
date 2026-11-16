"""
API Integration Tests for FastAPI Backend
Run with: pytest backend/test_api.py
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["offline_ready"] is True
    assert data["total_historical_days"] == 670
    assert "Bengaluru" in data["city"]


def test_city_summary():
    response = client.get("/api/city/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Bengaluru"
    assert data["latest_date"] == "2024-10-31"
    assert data["city_aqi"] is not None
    assert 0 <= data["city_aqi"] <= 500
    assert data["category"] in ("Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe")
    assert "sparkline_14d" in data
    assert len(data["sparkline_14d"]) == 14
    assert data["reporting_stations_count"] >= 10


def test_get_stations():
    response = client.get("/api/stations")
    assert response.status_code == 200
    stations = response.json()
    assert len(stations) == 14
    
    active = [s for s in stations if s["is_active"]]
    inactive = [s for s in stations if not s["is_active"]]
    assert len(active) == 13
    assert len(inactive) == 1
    assert inactive[0]["station_id"] == "site_164"
    assert inactive[0]["latest_category"] == "Decommissioned"


def test_get_station_summary():
    # Valid station: site_162 (BTM Layout)
    response = client.get("/api/stations/site_162/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["metadata"]["station_id"] == "site_162"
    assert len(data["history"]) > 0

    # Non-existent station
    bad_resp = client.get("/api/stations/non_existent_site/summary")
    assert bad_resp.status_code == 404


def test_analytics_trends():
    response = client.get("/api/analytics/trends?start_date=2024-01-01&end_date=2024-01-31")
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 31
    assert records[0]["date"] == "2024-01-01"
    assert records[-1]["date"] == "2024-01-31"


def test_analytics_weather_impact():
    response = client.get("/api/analytics/weather-impact")
    assert response.status_code == 200
    data = response.json()
    assert "correlation_matrix" in data
    assert "key_findings" in data
    assert len(data["key_findings"]) >= 3


def test_analytics_diurnal():
    response = client.get("/api/analytics/diurnal")
    assert response.status_code == 200
    data = response.json()
    assert "BTM Layout" in data
    assert "Peenya" in data
    assert "diurnal_curves" in data["BTM Layout"]


def test_forecast_backtest():
    response = client.get("/api/forecast/backtest")
    assert response.status_code == 200
    data = response.json()
    assert "model_comparison" in data
    assert len(data["model_comparison"]) == 4
    assert "top_features" in data
    assert "test_timeline" in data
    assert len(data["test_timeline"]) == 123


def test_transparency_ledger():
    response = client.get("/api/transparency")
    assert response.status_code == 200
    data = response.json()
    assert data["audit_metrics"]["total_raw_daily_records"] == 50584
    assert data["audit_metrics"]["compliant_daily_records_preserved"] == 46795
    assert data["data_provenance"]["city"] == "Bengaluru, Karnataka, India"


def test_frontend_static_serving():
    """Verify that root / serves index.html and assets are reachable."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "BreatheWise" in response.text


def test_ai_expansion_routes_presence():
    """Verify that all four Phase B, C, and D routes are wired and responsive."""
    # 1. AI Insights (Phase B)
    res_insights = client.get("/api/ai/insights?station_id=city_composite&date=2024-10-31")
    assert res_insights.status_code == 200
    assert res_insights.json()["status"] == "success"

    # 2. AI Regimes (Phase C)
    res_regimes = client.get("/api/ai/regimes")
    assert res_regimes.status_code == 200
    assert res_regimes.json()["status"] == "success"

    # 3. AI Health Advisory (Phase D)
    res_health = client.get("/api/ai/health-advisory?station_id=city_composite&date=2024-10-31")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "success"

    # 4. Purification Simulator (Phase D)
    res_purify = client.post("/api/purification/simulate", json={
        "room_area_m2": 20.0,
        "ceiling_height_m": 2.8,
        "initial_pm25_ug_m3": 67.7,
        "cadr_m3_h": 300.0,
        "runtime_hours": 2.0
    })
    assert res_purify.status_code == 200
    assert res_purify.json()["status"] == "success"

