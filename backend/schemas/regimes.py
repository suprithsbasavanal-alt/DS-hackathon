"""
BreatheWise Pydantic v2 validation contracts for Exploratory Environmental Regimes.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class DiagnosticMetrics(BaseModel):
    n_samples: int = Field(..., description="Total calendar days evaluated (670 days)")
    feature_dim: int = Field(8, description="Number of standardized input features (d=8, scalar wind speed excluded)")
    k_evaluated: List[int] = Field(default_factory=lambda: [2, 3, 4, 5])
    optimal_k: int = Field(3, description="Optimal cluster count chosen via silhouette optimization")
    silhouette_score: float = Field(..., description="Mean silhouette score for optimal k (0.3557)")
    min_cluster_size_pct: float = Field(..., description="Percentage of samples in smallest cluster (19.40%)")
    cluster_inertia: float = Field(..., description="Total within-cluster sum of squared distances (2601.0)")
    cluster_sizes: List[int] = Field(..., description="Sample counts in each cluster [338, 130, 202]")
    multi_seed_stability_ari: float = Field(1.0000, description="Mean pairwise Adjusted Rand Index across 5 diverse seeds")


class AcceptanceHeuristic(BaseModel):
    min_silhouette: float = Field(0.30, description="Analytical project acceptance threshold")
    min_cluster_size_pct: float = Field(5.0, description="Minimum cluster size threshold percentage")
    status: str = Field("heuristic_passed", description="Evaluation status of acceptance heuristic")
    note: str = Field(
        "Project-defined analytical acceptance heuristic, not physical proof of cluster reality.",
        description="Scientific humility disclosure"
    )


class RegimeProfileItem(BaseModel):
    cluster_id: int = Field(..., description="Cluster index (0, 1, 2)")
    name: str = Field(..., description="Descriptive observational pattern label")
    description: str = Field(..., description="Detailed meteorological and air quality pattern description")
    sample_count: int = Field(..., description="Number of historical days matching this pattern")
    sample_percentage: float = Field(..., description="Percentage of total historical record")
    dominant_months: List[str] = Field(..., description="Months with highest historical representation")
    centroid: Dict[str, float] = Field(..., description="Mean values across standardized features")
    mean_aqi: float = Field(..., description="Historical mean composite AQI for this cluster")
    mean_category: str = Field(..., description="CPCB health category corresponding to mean AQI")
    quantiles: Optional[Dict[str, Dict[str, float]]] = Field(
        None,
        description="Empirical distribution quantiles (min, 25th, median, 75th, max) for AQI and key criteria pollutants"
    )


class EnvironmentalRegimesResponse(BaseModel):
    status: str = Field("success", description="API response status")
    is_fallback: bool = Field(False, description="True if clustering failed stability criteria and fell back to deterministic seasonal grouping")
    diagnostic_metrics: DiagnosticMetrics
    acceptance_heuristic: AcceptanceHeuristic
    regimes: List[RegimeProfileItem]
    disclaimer: str = Field(
        "Exploratory atmospheric groupings based on standardized observations. "
        "Does not establish pollutant source attribution or physical causation.",
        description="Mandatory non-causal disclaimer"
    )
