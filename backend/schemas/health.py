"""
BreatheWise Pydantic v2 validation contracts for Deterministic Health Advisories.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class SensitiveGroupAdvice(BaseModel):
    asthma: str = Field(..., description="Targeted guidance for asthmatics and individuals with respiratory disease")
    elderly_and_children: str = Field(..., description="Targeted guidance for elderly cohorts and children")
    outdoor_workers: str = Field(..., description="Targeted guidance for outdoor workers and manual laborers")


class TriggeredAdvisoryItem(BaseModel):
    rule_id: str = Field(..., description="Deterministic rule identifier (e.g. RULE-AQI-MOD-01)")
    category: str = Field(..., description="CPCB health category or pollutant alert type")
    trigger_metric: str = Field(..., description="Human-readable trigger condition (e.g. 'City AQI: 141 (Moderate)')")
    trigger_value: float = Field(..., description="Exact metric value triggering the advisory")
    general_public_advice: str = Field(..., description="Actionable health guidance for the general public")
    sensitive_groups_advice: SensitiveGroupAdvice = Field(..., description="Actionable health guidance for sensitive groups")
    outdoor_activity_recommendation: str = Field(..., description="Clear recommendation for outdoor sports and exercise")


class HealthAdvisoryResponse(BaseModel):
    status: str = Field("success", description="API response status")
    evaluation_date: Optional[str] = Field(None, description="Observation date (null if evaluating custom hypothetical AQI)")
    station_id: Optional[str] = Field(None, description="Station ID (null if evaluating custom hypothetical AQI)")
    is_hypothetical: bool = Field(False, description="True if evaluating user-entered hypothetical AQI")
    aqi: float = Field(..., description="Evaluated AQI value")
    category: str = Field(..., description="CPCB 6-tier category corresponding to evaluated AQI")
    prominent_pollutant: Optional[str] = Field(None, description="Prominent pollutant driving the advisory")
    advisories: List[TriggeredAdvisoryItem] = Field(..., description="Deterministic advisories triggered by current state")
    medical_disclaimer: str = Field(
        "General public health information based on CPCB guidance. Not individualized medical advice.",
        description="Mandatory non-medical disclaimer"
    )
