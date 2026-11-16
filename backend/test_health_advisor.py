"""
Unit and Integration Tests for BreatheWise Deterministic Health Advisory Engine
Authoritative Reference: CPCB Table 3.2 Guidelines
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.health_advisor import evaluate_health_advisories, AQI_CATEGORY_RULES


@pytest.fixture
def client():
    return TestClient(app)


def test_cpcb_category_mappings_and_rule_ids():
    """Verify that every standard AQI band deterministically maps to its respective CPCB rule ID."""
    test_cases = [
        (25.0, "Good", "RULE-AQI-GOOD-01"),
        (75.0, "Satisfactory", "RULE-AQI-SAT-01"),
        (150.0, "Moderate", "RULE-AQI-MOD-01"),
        (250.0, "Poor", "RULE-AQI-POOR-01"),
        (350.0, "Very Poor", "RULE-AQI-VPOOR-01"),
        (450.0, "Severe", "RULE-AQI-SEV-01"),
    ]
    for aqi, expected_cat, expected_rule_id in test_cases:
        res = evaluate_health_advisories(aqi=aqi)
        assert res.category == expected_cat
        assert len(res.advisories) >= 1
        primary = res.advisories[0]
        assert primary.rule_id == expected_rule_id
        assert primary.category == expected_cat
        assert primary.sensitive_groups_advice.asthma != ""
        assert primary.sensitive_groups_advice.elderly_and_children != ""
        assert primary.sensitive_groups_advice.outdoor_workers != ""


def test_pollutant_threshold_alerts():
    """Verify that exceeding individual pollutant thresholds appends the specific alert rule."""
    pollutants = {
        "PM2.5": 75.0,  # Exceeds 60
        "PM10": 140.0,  # Exceeds 100
        "NO2": 52.0     # Exceeds 40
    }
    res = evaluate_health_advisories(aqi=150.0, pollutants=pollutants)
    rule_ids = [a.rule_id for a in res.advisories]
    assert "RULE-AQI-MOD-01" in rule_ids
    assert "RULE-PM25-ELEV-01" in rule_ids
    assert "RULE-PM10-ELEV-01" in rule_ids
    assert "RULE-NO2-RUSH-01" in rule_ids


def test_pollutant_threshold_non_trigger():
    """Verify that sub-threshold pollutant values do not trigger supplemental alert rules."""
    pollutants = {
        "PM2.5": 30.0,  # <= 60
        "PM10": 60.0,   # <= 100
        "NO2": 25.0     # <= 40
    }
    res = evaluate_health_advisories(aqi=45.0, pollutants=pollutants)
    rule_ids = [a.rule_id for a in res.advisories]
    assert rule_ids == ["RULE-AQI-GOOD-01"]


def test_aqi_clamping():
    """Verify out-of-range AQI values clamp properly without crash."""
    res_neg = evaluate_health_advisories(aqi=-50.0)
    assert res_neg.aqi == 0.0
    assert res_neg.category == "Good"

    res_high = evaluate_health_advisories(aqi=999.0)
    assert res_high.aqi == 500.0
    assert res_high.category == "Severe"


def test_medical_disclaimer():
    """Verify that the required non-medical disclaimer is present."""
    res = evaluate_health_advisories(aqi=120.0)
    assert "Not individualized medical advice" in res.medical_disclaimer


def test_endpoint_hypothetical_aqi(client):
    """Test GET /api/ai/health-advisory with explicit hypothetical aqi parameter."""
    resp = client.get("/api/ai/health-advisory?aqi=245.0")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["is_hypothetical"] is True
    assert data["aqi"] == 245.0
    assert data["category"] == "Poor"
    assert data["advisories"][0]["rule_id"] == "RULE-AQI-POOR-01"


def test_endpoint_historical_observation(client):
    """Test GET /api/ai/health-advisory reading from historical data for city_composite."""
    resp = client.get("/api/ai/health-advisory?station_id=city_composite&date=2024-10-31")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["is_hypothetical"] is False
    assert data["station_id"] == "city_composite"
    assert data["evaluation_date"] == "2024-10-31"
    assert data["aqi"] is not None
    assert len(data["advisories"]) >= 1
