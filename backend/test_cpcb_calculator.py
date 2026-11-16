"""
Unit Tests for CPCB Official IND-AQI Calculation Engine
Run with: pytest backend/test_cpcb_calculator.py
"""

import pytest
from backend.cpcb_calculator import (
    calculate_subindex_official_cpcb,
    get_aqi_category,
    get_aqi_category_meta,
    calculate_station_aqi,
    OFFICIAL_CLOSED_BREAKPOINTS,
    OFFICIAL_SEVERE_LOWER_THRESHOLDS
)


class TestCPCBSubIndexInterpolation:
    """Tests piecewise linear interpolation for categories 1 to 5."""
    
    @pytest.mark.parametrize("conc,expected,desc", [
        (0.0, 0.0, "Good lower bound"),
        (15.0, 25.0, "Good mid"),
        (30.0, 50.0, "Good upper bound"),
        (45.0, 75.5, "Satisfactory mid"),
        (60.0, 100.0, "Satisfactory upper bound"),
        (75.0, 150.5, "Moderate mid"),
        (90.0, 200.0, "Moderate upper bound"),
        (105.0, 250.5, "Poor mid"),
        (120.0, 300.0, "Poor upper bound"),
        (185.0, 350.5, "Very Poor mid"),
        (250.0, 400.0, "Very Poor upper bound / Severe lower threshold"),
    ])
    def test_pm25_piecewise_interpolation(self, conc, expected, desc):
        sub = calculate_subindex_official_cpcb("PM2.5", conc)
        assert sub is not None, f"Sub-index should not be None for {desc}"
        assert abs(sub - expected) < 0.2, f"Failed {desc}: got {sub}, expected {expected}"

    @pytest.mark.parametrize("pollutant,conc,expected_cat", [
        ("PM10", 25.0, "Good"),
        ("PM10", 75.0, "Satisfactory"),
        ("PM10", 175.0, "Moderate"),
        ("PM10", 300.0, "Poor"),
        ("PM10", 390.0, "Very Poor"),
        ("NO2", 20.0, "Good"),
        ("NO2", 60.0, "Satisfactory"),
        ("NO2", 130.0, "Moderate"),
        ("SO2", 20.0, "Good"),
        ("CO", 0.5, "Good"),
        ("O3", 25.0, "Good"),
        ("NH3", 100.0, "Good"),
        ("Pb", 0.25, "Good"),
    ])
    def test_all_pollutants_bracket_validity(self, pollutant, conc, expected_cat):
        sub = calculate_subindex_official_cpcb(pollutant, conc)
        assert sub is not None
        cat = get_aqi_category(sub)
        assert cat == expected_cat


class TestSevereRangeProjectPolicy:
    """
    Tests Project Implementation Policy: Severe values reported at 500 ceiling cap.
    Adheres to CPCB Table 3.2 open-ended Severe definitions.
    """
    
    @pytest.mark.parametrize("pollutant,conc,expected_sub,expected_cat,desc", [
        ("PM2.5", 250.0, 400.0, "Very Poor", "Exact Severe lower threshold"),
        ("PM2.5", 250.1, 500.0, "Severe", "Immediately above Severe threshold"),
        ("PM2.5", 300.0, 500.0, "Severe", "Well inside Severe range"),
        ("PM2.5", 893.0, 500.0, "Severe", "Extreme saturation spike (officially capped)"),
        ("PM10", 430.0, 400.0, "Very Poor", "Exact Severe lower threshold"),
        ("PM10", 430.1, 500.0, "Severe", "Immediately above Severe threshold"),
        ("PM10", 650.0, 500.0, "Severe", "Extreme PM10 spike (officially capped)"),
        ("NO2", 400.0, 400.0, "Very Poor", "Exact Severe lower threshold"),
        ("NO2", 400.1, 500.0, "Severe", "Immediately above Severe threshold"),
        ("SO2", 1600.0, 400.0, "Very Poor", "Exact Severe lower threshold"),
        ("SO2", 1600.1, 500.0, "Severe", "Immediately above Severe threshold"),
    ])
    def test_severe_threshold_and_ceiling(self, pollutant, conc, expected_sub, expected_cat, desc):
        sub = calculate_subindex_official_cpcb(pollutant, conc)
        cat = get_aqi_category(sub)
        assert abs(sub - expected_sub) < 0.2, f"Failed {desc}: got {sub}, expected {expected_sub}"
        assert cat == expected_cat, f"Failed category for {desc}: got {cat}, expected {expected_cat}"


class TestEdgeCasesAndValidation:
    """Tests sensor error handling, unsupported parameters, and nulls."""
    
    def test_negative_concentration(self):
        assert calculate_subindex_official_cpcb("PM2.5", -10.0) is None

    def test_none_concentration(self):
        assert calculate_subindex_official_cpcb("PM2.5", None) is None

    def test_unsupported_pollutant(self):
        with pytest.raises(ValueError):
            calculate_subindex_official_cpcb("UnknownGas", 50.0)

    def test_category_metadata(self):
        meta = get_aqi_category_meta(45.0)
        assert meta["name"] == "Good"
        assert meta["color"] == "#10B981"


class TestStationAQIRules:
    """Tests CPCB Station AQI rules, worst pollutant max operator, and CO/O3 exclusion."""
    
    def test_valid_station_calculation(self):
        # PM2.5 = 75.0 (Moderate: ~150.5), NO2 = 45.0 (Satisfactory: ~57.2), SO2 = 15.0 (Good: ~18.8)
        aqi, prom, subs = calculate_station_aqi({"PM2.5": 75.0, "NO2": 45.0, "SO2": 15.0})
        assert aqi in (150, 151)
        assert prom == "PM2.5"
        assert len(subs) == 3

    def test_minimum_three_pollutants_rule(self):
        # Only 2 pollutants -> Should return None
        aqi, prom, subs = calculate_station_aqi({"PM2.5": 75.0, "NO2": 45.0})
        assert aqi is None
        assert prom is None

    def test_particulate_requirement_rule(self):
        # 3 pollutants, but NO particulate matter (PM2.5 or PM10) -> Should return None
        aqi, prom, subs = calculate_station_aqi({"NO2": 45.0, "SO2": 15.0, "NH3": 25.0})
        assert aqi is None
        assert prom is None

    def test_co_o3_daily_exclusion(self):
        # When exclude_co_o3_daily=True, CO and O3 are ignored for daily station AQI
        data = {
            "PM2.5": 75.0,
            "NO2": 45.0,
            "CO": 0.8,
            "O3": 35.0
        }
        # Only PM2.5 and NO2 remain valid for daily AQI -> only 2 valid criteria -> should be None
        aqi, prom, subs = calculate_station_aqi(data, exclude_co_o3_daily=True)
        assert aqi is None
        assert "CO" not in subs
        assert "O3" not in subs

        # If SO2 is added, valid count becomes 3 (PM2.5, NO2, SO2) -> station AQI valid
        data["SO2"] = 20.0
        aqi, prom, subs = calculate_station_aqi(data, exclude_co_o3_daily=True)
        assert aqi is not None
        assert prom == "PM2.5"
        assert "CO" not in subs
        assert "O3" not in subs
