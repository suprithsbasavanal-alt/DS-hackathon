"""
Comprehensive Unit and Regression Tests for Phase C:
Exploratory Environmental Regimes, k-Means Optimization, ARI Stability, and Quantile Fallback.

Run with: pytest backend/test_regimes.py
"""

import json
import pytest
import pandas as pd
from fastapi.testclient import TestClient
from backend.main import app
from backend.environmental_regimes import (
    FEATURE_COLS,
    SEEDS_FOR_STABILITY,
    REGIME_DESCRIPTIONS,
    prepare_feature_dataframe,
    evaluate_kmeans_clustering,
    compute_deterministic_seasonal_fallback,
    compute_distribution_quantiles,
    build_regimes_payload,
    get_environmental_regimes,
)
from backend.schemas.regimes import EnvironmentalRegimesResponse

client = TestClient(app)


@pytest.fixture(scope="module")
def city_data():
    with open("data/processed/city_daily_summary.json", "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def feature_df(city_data):
    return prepare_feature_dataframe(city_data)


# =====================================================================
# 1. Feature Matrix & Wind Orthogonality Verification
# =====================================================================

def test_feature_matrix_orthogonality_and_completeness(feature_df):
    """
    CRITICAL ACCEPTANCE GATE:
    1. Feature matrix contains exactly d=8 standardized features.
    2. Scalar wind speed is deliberately excluded to prevent redundant collinear double-weighting.
    3. Exactly 670 calendar days with zero missing values (100% complete).
    """
    assert len(FEATURE_COLS) == 8
    assert "wind_speed_resultant" not in FEATURE_COLS
    assert "wind_u" in FEATURE_COLS
    assert "wind_v" in FEATURE_COLS

    # Check total rows
    assert len(feature_df) == 670

    # Check completeness (0 missing values across all 8 features)
    for col in FEATURE_COLS:
        null_count = feature_df[col].isnull().sum()
        assert null_count == 0, f"Found {null_count} nulls in feature '{col}'"


# =====================================================================
# 2. k-Means Clustering Optimization & Silhouette Peak
# =====================================================================

def test_kmeans_optimization_and_silhouette_peak(feature_df):
    """
    CRITICAL ACCEPTANCE GATE:
    1. Evaluates k in [2, 3, 4, 5].
    2. k=3 is the optimal silhouette peak (S ~ 0.3557).
    3. Minimum cluster size is 19.4% (130 days), well above the 5.0% threshold.
    """
    diag, models, passed = evaluate_kmeans_clustering(feature_df, random_state=42)

    assert diag.n_samples == 670
    assert diag.feature_dim == 8
    assert diag.k_evaluated == [2, 3, 4, 5]
    assert diag.optimal_k == 3
    assert 0.35 <= diag.silhouette_score <= 0.37
    assert 19.0 <= diag.min_cluster_size_pct <= 20.0
    assert 2550.0 <= diag.cluster_inertia <= 2650.0
    assert sum(diag.cluster_sizes) == 670
    assert passed is True


# =====================================================================
# 3. Multi-Seed Stability (Adjusted Rand Index)
# =====================================================================

def test_multi_seed_stability_ari(feature_df):
    """
    CRITICAL ACCEPTANCE GATE:
    Pairwise Adjusted Rand Index (ARI) = 1.0000 across seeds [42, 100, 2024, 7, 99].
    Proves that the k=3 cluster partition is invariant to random centroid initialization.
    """
    diag, _, _ = evaluate_kmeans_clustering(feature_df, random_state=42)
    assert diag.multi_seed_stability_ari == 1.0000


# =====================================================================
# 4. Acceptance Heuristic & Non-Causal Descriptive Labels
# =====================================================================

def test_acceptance_heuristic_and_descriptive_labels():
    """
    CRITICAL ACCEPTANCE GATE:
    1. S >= 0.30 acceptance heuristic is passed.
    2. Note explicitly frames it as an analytical project acceptance heuristic, not physical proof.
    3. Clusters use strictly descriptive observational labels (zero causal source claims).
    4. REGRESSION GUARD: Cluster descriptions must NOT contain mechanistic or causal phrases
       such as 'ventilation and wet scavenging', 'convective conditions', or 'boundary layer stabilization'.
    """
    payload = build_regimes_payload(force_fallback=False)
    assert payload["is_fallback"] is False

    heuristic = payload["acceptance_heuristic"]
    assert heuristic["min_silhouette"] == 0.30
    assert heuristic["status"] == "heuristic_passed"
    assert "heuristic" in heuristic["note"].lower()

    regimes = payload["regimes"]
    assert len(regimes) == 3

    names = [r["name"] for r in regimes]
    assert "Monsoon and high-ventilation pattern" in names
    assert "Hot/dry summer-transition pattern" in names
    assert "Winter/post-monsoon pattern" in names

    # Prohibited mechanistic and causal phrases
    prohibited_phrases = [
        "ventilation and wet scavenging",
        "active atmospheric ventilation",
        "convective conditions",
        "boundary layer stabilization",
        "pollution source attribution",
    ]
    for r in regimes:
        desc = r["description"].lower()
        for phrase in prohibited_phrases:
            assert phrase not in desc, f"Found prohibited mechanistic phrase '{phrase}' in description: {r['description']}"

    # Disclaimer check
    assert "Exploratory atmospheric groupings" in payload["disclaimer"]
    assert "Does not establish pollutant source attribution" in payload["disclaimer"]


# =====================================================================
# 5. Deterministic Seasonal Fallback & Quantile Verification
# =====================================================================

def test_deterministic_seasonal_fallback_completeness(feature_df):
    """
    CRITICAL ACCEPTANCE GATE:
    1. Deterministic Seasonal Fallback partitions all 670 daily observations into 3 calendar seasons:
       - Monsoon (Jun–Sep): N = 244 (36.42%)
       - Pre-Monsoon Summer (Mar–May): N = 184 (27.46%)
       - Post-Monsoon & Winter (Oct–Feb): N = 242 (36.12%)
    2. Partitions are mutually exclusive and collectively exhaustive: sum of days = 670.
    3. Empirical distribution quantiles (min, 25th, median, 75th, max) are explicitly computed.
    4. Deterministic repeatability: multiple invocations yield identical results.
    """
    profiles_1 = compute_deterministic_seasonal_fallback(feature_df)
    profiles_2 = compute_deterministic_seasonal_fallback(feature_df)

    assert len(profiles_1) == 3
    assert len(profiles_2) == 3

    # Total sample completeness
    total_samples = sum(p.sample_count for p in profiles_1)
    assert total_samples == 670

    # Specific partition sample counts
    counts_map = {p.name: p.sample_count for p in profiles_1}
    assert counts_map["Monsoon Seasonal Grouping (Deterministic Fallback)"] == 244
    assert counts_map["Pre-Monsoon Summer Seasonal Grouping (Deterministic Fallback)"] == 184
    assert counts_map["Post-Monsoon & Winter Seasonal Grouping (Deterministic Fallback)"] == 242

    # Verify empirical quantiles presence and ordering
    for p in profiles_1:
        assert p.quantiles is not None
        assert "city_aqi" in p.quantiles
        aqi_q = p.quantiles["city_aqi"]
        assert aqi_q["min"] <= aqi_q["q25"] <= aqi_q["median"] <= aqi_q["q75"] <= aqi_q["max"]
        assert "Deterministic Fallback" in p.name

    # Deterministic repeatability check
    for p1, p2 in zip(profiles_1, profiles_2):
        assert p1.model_dump() == p2.model_dump()

    # Forced fallback payload check
    fallback_payload = build_regimes_payload(force_fallback=True)
    assert fallback_payload["is_fallback"] is True
    assert fallback_payload["acceptance_heuristic"]["status"] == "fallback_engaged"
    assert "deterministic seasonal fallback" in fallback_payload["acceptance_heuristic"]["note"].lower()
    assert len(fallback_payload["regimes"]) == 3
    for r in fallback_payload["regimes"]:
        assert "Deterministic Fallback" in r["name"]


# =====================================================================
# 6. GET /api/ai/regimes Endpoint Integration
# =====================================================================

def test_api_ai_regimes_endpoint_default():
    """Tests GET /api/ai/regimes returns HTTP 200 with valid optimal k=3 regimes."""
    response = client.get("/api/ai/regimes")
    assert response.status_code == 200
    data = response.json()

    # Schema validation via Pydantic
    parsed = EnvironmentalRegimesResponse(**data)
    assert parsed.status == "success"
    assert parsed.is_fallback is False
    assert parsed.diagnostic_metrics.optimal_k == 3
    assert parsed.diagnostic_metrics.silhouette_score >= 0.30
    assert parsed.diagnostic_metrics.multi_seed_stability_ari == 1.0
    assert len(parsed.regimes) == 3


def test_api_ai_regimes_endpoint_force_fallback():
    """Tests GET /api/ai/regimes?force_fallback=true returns deterministic seasonal fallback."""
    response = client.get("/api/ai/regimes?force_fallback=true")
    assert response.status_code == 200
    data = response.json()

    parsed = EnvironmentalRegimesResponse(**data)
    assert parsed.status == "success"
    assert parsed.is_fallback is True
    assert parsed.acceptance_heuristic.status == "fallback_engaged"
    assert len(parsed.regimes) == 3
    for r in parsed.regimes:
        assert "Fallback" in r.name
