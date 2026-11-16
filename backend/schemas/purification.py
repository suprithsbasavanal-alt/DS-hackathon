"""
BreatheWise Pydantic v2 validation contracts for Air Purification Physics Simulator.
"""

from typing import List
from pydantic import BaseModel, Field


class DecayPoint(BaseModel):
    time_hours: float = Field(..., description="Elapsed runtime in hours")
    pm25_ug_m3: float = Field(..., description="Indoor PM2.5 concentration at this time (µg/m³)")
    reduction_pct: float = Field(..., description="Cumulative percentage reduction from initial concentration")


class PurificationSimulationRequest(BaseModel):
    room_area_m2: float = Field(20.0, ge=5.0, le=200.0, description="Room floor area in square meters (5.0 to 200.0)")
    ceiling_height_m: float = Field(2.8, ge=2.0, le=5.0, description="Ceiling height in meters (2.0 to 5.0)")
    initial_pm25_ug_m3: float = Field(67.7, ge=5.0, le=1000.0, description="Initial indoor PM2.5 in µg/m³ (5.0 to 1000.0)")
    cadr_m3_h: float = Field(300.0, ge=0.0, le=1200.0, description="Clean Air Delivery Rate in m³/h (0.0 to 1200.0; CADR=0 supported)")
    runtime_hours: float = Field(2.0, ge=0.0, le=12.0, description="Purifier runtime in hours (0.0 to 12.0; t=0 supported)")


class PurificationSimulationResponse(BaseModel):
    status: str = Field("success", description="API response status")
    room_area_m2: float = Field(..., description="Validated floor area (m²)")
    ceiling_height_m: float = Field(..., description="Validated ceiling height (m)")
    room_volume_m3: float = Field(..., description="Calculated room volume V = A * h (m³)")
    initial_pm25_ug_m3: float = Field(..., description="Starting indoor PM2.5 concentration (µg/m³)")
    initial_pm25_source: str = Field(
        "Initialized from outdoor city composite observation (2024-10-31) in the absence of indoor sensors. User-adjustable.",
        description="Transparency statement on initial concentration source"
    )
    cadr_m3_h: float = Field(..., description="Clean Air Delivery Rate (m³/h)")
    runtime_hours: float = Field(..., description="Runtime duration (hours)")
    air_changes_per_hour_cadr: float = Field(..., description="Equivalent CADR air changes per hour: ACH = CADR / V")
    final_pm25_ug_m3: float = Field(..., description="Calculated final PM2.5 concentration: C(t) = C0 * exp(-(CADR/V)*t)")
    percentage_reduction: float = Field(..., description="Calculated reduction percentage: (1 - C(t)/C0) * 100")
    decay_curve: List[DecayPoint] = Field(..., description="40 evenly spaced points along [0, t] for smooth curve rendering")
    formula_used: str = Field("C(t) = C0 * exp(-(CADR / V) * t)", description="Idealized first-order exponential decay formula")
    assumptions_ledger: List[str] = Field(
        default_factory=lambda: [
            "Instantaneous and perfect spatial mixing throughout the room volume (no dead zones or localized concentration gradients).",
            "Zero continuing indoor emission sources (no cooking, smoking, incense, or dust resuspension).",
            "Zero building envelope infiltration/exfiltration through doors, windows, and cracks (ACH_nat = 0).",
            "Zero natural particle deposition, gravitational settling, or wall adsorption losses.",
            "Continuous operation at rated Clean Air Delivery Rate (CADR) with a clean filter and zero bypass."
        ],
        description="Exhaustive ledger of 5 idealizing assumptions"
    )
    disclaimer: str = Field(
        "Theoretical first-order mass-balance scenario. Not an indoor sensor reading, not an AI prediction, and not a measured purifier test.",
        description="Mandatory simulation disclaimer"
    )
