"""
Unit and Integration Tests for BreatheWise Theoretical Purification Simulator
Model Identifier: PHYS-PURIFIER-01
Authoritative Reference: Idealized First-Order Mass-Balance Exponential Decay
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.purification_simulator import simulate_purification, ASSUMPTIONS_LEDGER


@pytest.fixture
def client():
    return TestClient(app)


def test_purifier_boundary_zero_runtime():
    """Verify that runtime=0 yields zero reduction and final concentration equals initial concentration."""
    res = simulate_purification(
        room_area_m2=20.0,
        ceiling_height_m=2.8,
        initial_pm25_ug_m3=80.0,
        cadr_m3_h=300.0,
        runtime_hours=0.0
    )
    assert res.final_pm25_ug_m3 == 80.0
    assert res.percentage_reduction == 0.0
    assert len(res.decay_curve) == 40
    assert res.decay_curve[0].pm25_ug_m3 == 80.0
    assert res.decay_curve[-1].pm25_ug_m3 == 80.0


def test_purifier_boundary_zero_cadr():
    """Verify that CADR=0 yields zero reduction and concentration remains unchanged."""
    res = simulate_purification(
        room_area_m2=20.0,
        ceiling_height_m=2.8,
        initial_pm25_ug_m3=95.0,
        cadr_m3_h=0.0,
        runtime_hours=3.0
    )
    assert res.final_pm25_ug_m3 == 95.0
    assert res.percentage_reduction == 0.0
    assert res.air_changes_per_hour_cadr == 0.0
    for pt in res.decay_curve:
        assert pt.pm25_ug_m3 == 95.0
        assert pt.reduction_pct == 0.0


def test_purifier_standard_decay():
    """Verify standard operational decay calculation against theoretical physics formula."""
    res = simulate_purification(
        room_area_m2=20.0,
        ceiling_height_m=2.8,
        initial_pm25_ug_m3=67.7,
        cadr_m3_h=300.0,
        runtime_hours=2.0
    )
    assert res.room_volume_m3 == 56.0
    assert res.air_changes_per_hour_cadr == round(300.0 / 56.0, 2)  # ~5.36 ACH
    assert res.final_pm25_ug_m3 < 1.0  # Decays by >99% after 10.7 air changes
    assert res.percentage_reduction > 99.0


def test_purifier_monotonic_decay():
    """Verify that concentrations along the 40-point curve monotonically decrease when CADR > 0."""
    res = simulate_purification(
        room_area_m2=35.0,
        ceiling_height_m=3.0,
        initial_pm25_ug_m3=150.0,
        cadr_m3_h=250.0,
        runtime_hours=2.5
    )
    assert len(res.decay_curve) == 40
    prev_conc = res.decay_curve[0].pm25_ug_m3
    assert prev_conc == 150.0
    for pt in res.decay_curve[1:]:
        assert pt.pm25_ug_m3 <= prev_conc
        prev_conc = pt.pm25_ug_m3


def test_purifier_disclosures_and_assumptions():
    """Verify that all five idealizing assumptions and physics disclaimers are preserved."""
    res = simulate_purification()
    assert len(res.assumptions_ledger) == 5
    assert "Instantaneous and perfect spatial mixing" in res.assumptions_ledger[0]
    assert "Not an indoor sensor reading" in res.disclaimer
    assert "C(t) = C0 * exp(-(CADR / V) * t)" in res.formula_used


def test_purifier_validation_errors():
    """Verify that non-positive room geometry raises ValueError."""
    with pytest.raises(ValueError, match="strictly positive"):
        simulate_purification(room_area_m2=-10.0)

    with pytest.raises(ValueError, match="strictly positive"):
        simulate_purification(ceiling_height_m=0.0)

    with pytest.raises(ValueError, match="cannot be negative"):
        simulate_purification(cadr_m3_h=-50.0)


def test_endpoint_purification_simulate(client):
    """Test POST /api/purification/simulate endpoint with valid payload."""
    payload = {
        "room_area_m2": 25.0,
        "ceiling_height_m": 3.0,
        "initial_pm25_ug_m3": 75.0,
        "cadr_m3_h": 350.0,
        "runtime_hours": 1.5
    }
    resp = client.post("/api/purification/simulate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["room_volume_m3"] == 75.0
    assert len(data["decay_curve"]) == 40
    assert len(data["assumptions_ledger"]) == 5
    assert "Not an indoor sensor reading" in data["disclaimer"]


def test_endpoint_purification_validation(client):
    """Test POST /api/purification/simulate endpoint returns 422 on invalid input."""
    payload = {
        "room_area_m2": -20.0,
        "ceiling_height_m": 2.8,
        "initial_pm25_ug_m3": 67.7,
        "cadr_m3_h": 300.0,
        "runtime_hours": 2.0
    }
    resp = client.post("/api/purification/simulate", json=payload)
    assert resp.status_code == 422
