"""
Comprehensive Unit and Regression Tests for Phase B:
Environmental Foundation, Pollutant Thresholds, and API Contracts.

Run with: pytest backend/test_environmental.py
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.threshold_engine import (
    evaluate_single_pollutant,
    evaluate_all_criteria_pollutants,
    POLLUTANT_STANDARD_UNITS,
    POLLUTANT_DISPLAY_NAMES,
)
from backend.environmental_analysis import (
    compute_wind_components,
    compute_retrospective_correlations,
    get_environmental_insights,
)
from backend.schemas.environmental import EnvironmentalInsightsResponse

client = TestClient(app)


# =====================================================================
# 1. Threshold Engine Unit Tests
# =====================================================================

def test_threshold_engine_valid_units():
    """Verifies that all criteria pollutants require their standard CPCB physical units."""
    # PM2.5 in ug/m3
    item_pm25 = evaluate_single_pollutant("PM2.5", 45.0, unit="µg/m³")
    assert item_pm25.unit == "µg/m³"
    assert item_pm25.display_name == "PM₂.₅"

    # CO in mg/m3
    item_co = evaluate_single_pollutant("CO", 0.8, unit="mg/m³")
    assert item_co.unit == "mg/m³"
    assert item_co.display_name == "CO"


def test_threshold_engine_unit_mismatch_raises_error():
    """Verifies that mismatched units (e.g., CO in ppm or PM2.5 in mg/m3) raise ValueError."""
    with pytest.raises(ValueError, match="Unit mismatch"):
        evaluate_single_pollutant("CO", 1.5, unit="ppm")

    with pytest.raises(ValueError, match="Unit mismatch"):
        evaluate_single_pollutant("PM2.5", 45.0, unit="mg/m³")


def test_threshold_engine_cpcb_breakpoints():
    """Tests CPCB Table 3.2 interpolation across standard categories."""
    # PM2.5 Good: 15 ug/m3 -> sub-index = 25.0
    item_good = evaluate_single_pollutant("PM2.5", 15.0)
    assert item_good.sub_index == 25.0
    assert item_good.tier == "Good"

    # PM2.5 Moderate: 67.7 ug/m3 -> sub-index ~ 126.4
    item_mod = evaluate_single_pollutant("PM2.5", 67.7)
    assert item_mod.tier == "Moderate"
    assert 101.0 <= item_mod.sub_index <= 200.0

    # PM10 Satisfactory: 75.0 ug/m3 -> sub-index = 75.5
    item_sat = evaluate_single_pollutant("PM10", 75.0)
    assert item_sat.tier == "Satisfactory"
    assert 51.0 <= item_sat.sub_index <= 100.0

    # Severe range policy: PM2.5 > 250 -> 500.0 ceiling cap
    item_sev = evaluate_single_pollutant("PM2.5", 300.0)
    assert item_sev.sub_index == 500.0
    assert item_sev.tier == "Severe"


def test_threshold_engine_daily_co_o3_null_subindex():
    """
    CRITICAL ACCEPTANCE GATE: Daily 24h arithmetic daily means for CO and O3
    must return sub_index: null and tier: 'CPCB 8h standard only'.
    """
    co_item = evaluate_single_pollutant("CO", 0.95, is_daily=True)
    assert co_item.sub_index is None
    assert co_item.tier == "CPCB 8h standard only"
    assert co_item.is_valid is False
    assert co_item.is_informational is True
    assert "8-hour" in co_item.notes

    o3_item = evaluate_single_pollutant("O3", 42.1, is_daily=True)
    assert o3_item.sub_index is None
    assert o3_item.tier == "CPCB 8h standard only"
    assert o3_item.is_valid is False
    assert o3_item.is_informational is True
    assert "8-hour" in o3_item.notes


def test_threshold_engine_pb_transparency():
    """
    CRITICAL ACCEPTANCE GATE: Lead (Pb) is unmonitored and must return
    concentration: null, sub_index: null, and tier: 'Not available in supplied dataset'.
    Never zero or imputed.
    """
    pb_item = evaluate_single_pollutant("Pb", None, is_daily=True)
    assert pb_item.concentration is None
    assert pb_item.sub_index is None
    assert pb_item.tier == "Not available in supplied dataset"
    assert pb_item.is_valid is False
    assert pb_item.averaging_period == "Not monitored"


def test_threshold_engine_missing_and_negative_data():
    """Tests handling of missing values (None) and sensor glitches (negative readings)."""
    # Missing value
    missing_item = evaluate_single_pollutant("PM2.5", None)
    assert missing_item.concentration is None
    assert missing_item.sub_index is None
    assert missing_item.tier == "Missing Data"
    assert missing_item.is_valid is False

    # Negative sensor glitch
    glitch_item = evaluate_single_pollutant("PM10", -12.4)
    assert glitch_item.concentration == -12.4
    assert glitch_item.sub_index is None
    assert glitch_item.tier == "Invalid (Sensor Glitch)"
    assert glitch_item.is_valid is False


def test_threshold_engine_all_criteria_pollutants_canonical_order():
    """Tests evaluate_all_criteria_pollutants outputs 8 items in canonical CPCB order."""
    data = {
        "pm25": 45.0, "pm10": 85.0, "no2": 22.0, "so2": 12.0,
        "co": 0.7, "o3": 40.0, "nh3": 15.0
    }
    items = evaluate_all_criteria_pollutants(data, is_daily=True)
    assert len(items) == 8
    expected_names = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "NH3", "Pb"]
    assert [p.name for p in items] == expected_names


# =====================================================================
# 2. Environmental Analysis & Wind Decomposition Tests
# =====================================================================

def test_wind_orthogonal_decomposition():
    """Tests zonal (u) and meridional (v) vector calculation under meteorological convention."""
    # North wind (0 deg) -> wind blows southward: u = 0, v = -10
    u, v = compute_wind_components(10.0, 0.0)
    assert u == 0.0
    assert v == -10.0

    # East wind (90 deg) -> wind blows westward: u = -10, v = 0
    u, v = compute_wind_components(10.0, 90.0)
    assert u == -10.0
    assert v == 0.0

    # South wind (180 deg) -> wind blows northward: u = 0, v = 10
    u, v = compute_wind_components(10.0, 180.0)
    assert u == 0.0
    assert v == 10.0

    # West wind (270 deg) -> wind blows eastward: u = 10, v = 0
    u, v = compute_wind_components(10.0, 270.0)
    assert u == 10.0
    assert v == 0.0

    # Missing inputs
    assert compute_wind_components(None, 90.0) == (None, None)
    assert compute_wind_components(10.0, None) == (None, None)


def test_retrospective_correlations_integrity():
    """
    CRITICAL ACCEPTANCE GATE:
    1. Sample size N = 670 across all daily city composite correlations.
    2. Surface pressure exhibits retrospective positive correlation (r ~ +0.607).
    3. Phrasing is non-causal ('historically associated', no 'trapping' claims).
    """
    corrs = compute_retrospective_correlations()
    assert len(corrs) >= 9

    for c in corrs:
        assert c.n_samples == 670, f"Sample size mismatch for {c.metric_x} vs {c.metric_y}"
        assert -1.0 <= c.pearson_r <= 1.0
        assert -1.0 <= c.spearman_rho <= 1.0
        assert c.description is not None
        # Non-causal phrasing assertion
        desc_lower = c.description.lower()
        assert "cause" not in desc_lower or "does not" in desc_lower

    # Target: surface pressure vs city AQI
    p_corr = next(c for c in corrs if c.metric_x == "pressure_mean" and c.metric_y == "city_aqi")
    assert 0.60 <= p_corr.pearson_r <= 0.62
    assert 0.65 <= p_corr.spearman_rho <= 0.68
    assert "historically associated" in p_corr.description
    assert "does not prove" in p_corr.description


# =====================================================================
# 3. GET /api/ai/insights Endpoint Integration Tests
# =====================================================================

def test_api_ai_insights_city_composite_default():
    """Tests GET /api/ai/insights returns valid schema for default city composite and date."""
    response = client.get("/api/ai/insights")
    assert response.status_code == 200
    data = response.json()

    # Schema validation via Pydantic
    parsed = EnvironmentalInsightsResponse(**data)
    assert parsed.status == "success"
    assert parsed.date == "2024-10-31"
    assert parsed.is_historical is True
    assert parsed.station.id == "city_composite"
    assert parsed.aqi_summary.aqi == 141
    assert parsed.aqi_summary.category == "Moderate"

    # Pollutant checks
    assert len(parsed.pollutants) == 8
    pollutant_map = {p.name: p for p in parsed.pollutants}

    # PM2.5 & PM10
    assert pollutant_map["PM2.5"].sub_index is not None
    assert pollutant_map["PM10"].sub_index is not None

    # CO & O3 null sub-index check
    assert pollutant_map["CO"].sub_index is None
    assert pollutant_map["CO"].tier == "CPCB 8h standard only"
    assert pollutant_map["O3"].sub_index is None
    assert pollutant_map["O3"].tier == "CPCB 8h standard only"

    # Pb unmonitored check
    assert pollutant_map["Pb"].concentration is None
    assert pollutant_map["Pb"].sub_index is None
    assert pollutant_map["Pb"].tier == "Not available in supplied dataset"

    # Meteorology & Correlations Scope
    assert parsed.meteorology.pressure_mean is not None
    assert parsed.meteorology.wind_u is not None
    assert parsed.correlation_scope == "citywide_historical"
    assert len(parsed.correlations) >= 9
    for c in parsed.correlations:
        assert c.scope == "citywide_historical"
        assert "670" in c.scope_note


def test_api_ai_insights_active_station():
    """Tests GET /api/ai/insights for a specific active station (BTM Layout: site_162)."""
    response = client.get("/api/ai/insights?station_id=site_162&date=2024-10-31")
    assert response.status_code == 200
    data = response.json()
    assert data["station"]["id"] == "site_162"
    assert data["station"]["is_active"] is True
    assert len(data["pollutants"]) == 8
    assert data["correlation_scope"] == "citywide_historical"
    for c in data["correlations"]:
        assert c["scope"] == "citywide_historical"
        assert "not isolated to station" in c["scope_note"]


def test_api_ai_insights_decommissioned_station():
    """
    Tests GET /api/ai/insights for decommissioned station (site_164).
    Must return structured status: decommissioned with clear informational messaging.
    Correlations must be omitted to eliminate the risk of users interpreting citywide statistics
    as station-specific findings.
    """
    response = client.get("/api/ai/insights?station_id=site_164&date=2024-10-31")
    assert response.status_code == 200
    data = response.json()
    assert data["station"]["id"] == "site_164"
    assert data["station"]["is_active"] is False
    assert data["station"]["status"] == "decommissioned"
    assert data["aqi_summary"]["category"] == "Decommissioned"
    assert "decommissioned" in data["station"]["message"].lower()

    # Correlation omission check
    assert data["correlation_scope"] == "omitted"
    assert data["correlations"] == []
    assert data["data_integrity"]["correlations_omitted"] is True


def test_correlation_scope_demarcation():
    """
    REGRESSION TEST: Verifies explicit statistical scope labeling across all three request types:
    1. City composite: correlation_scope is 'citywide_historical', scope_note cites 670 daily records.
    2. Active station: correlation_scope is 'citywide_historical', scope_note explicitly clarifies it is regional baseline and NOT isolated to the station.
    3. Decommissioned station: correlation_scope is 'omitted', correlations list is strictly empty.
    """
    # 1. City composite
    res_city = client.get("/api/ai/insights?station_id=city_composite").json()
    assert res_city["correlation_scope"] == "citywide_historical"
    assert len(res_city["correlations"]) == 10
    assert all(c["scope"] == "citywide_historical" for c in res_city["correlations"])
    assert "670" in res_city["correlations"][0]["scope_note"]

    # 2. Active station
    res_st = client.get("/api/ai/insights?station_id=site_162&date=2024-10-31").json()
    assert res_st["correlation_scope"] == "citywide_historical"
    assert len(res_st["correlations"]) == 10
    assert all(c["scope"] == "citywide_historical" for c in res_st["correlations"])
    assert "not isolated to station 'site_162'" in res_st["correlations"][0]["scope_note"]

    # 3. Decommissioned station
    res_decom = client.get("/api/ai/insights?station_id=site_164&date=2024-10-31").json()
    assert res_decom["correlation_scope"] == "omitted"
    assert res_decom["correlations"] == []
    assert res_decom["data_integrity"]["correlations_omitted"] is True


def test_api_ai_insights_invalid_station_404():
    """Tests GET /api/ai/insights with unknown station ID returns HTTP 404."""
    response = client.get("/api/ai/insights?station_id=site_nonexistent_9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_api_ai_insights_invalid_date_404():
    """Tests GET /api/ai/insights with out-of-range date returns HTTP 404."""
    response = client.get("/api/ai/insights?date=2099-12-31")
    assert response.status_code == 404
    assert "no data available" in response.json()["detail"].lower()
