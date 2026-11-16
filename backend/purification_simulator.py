"""
BreatheWise - Theoretical Air Purification Simulator
Model Identifier: PHYS-PURIFIER-01
Authoritative Reference: Idealized First-Order Mass-Balance Exponential Decay Equation.

Mathematical Formulation:
V = A * h  (Room Volume in m³)
C(t) = C0 * exp(-(CADR / V) * t)  (PM2.5 concentration at time t in µg/m³)
Percentage Reduction = (1 - C(t) / C0) * 100%
ACH_CADR = CADR / V  (Equivalent air changes per hour)

Boundary Conditions & Edge Cases:
- t = 0 -> C(t) = C0, Reduction = 0.0%
- CADR = 0 -> C(t) = C0, Reduction = 0.0%
- V <= 0 -> Raises ValueError
- Generates 40 evenly spaced points along [0, t] for smooth Recharts rendering.
- Fully articulates the 5 idealizing physical assumptions.
"""

import math
from typing import List, Dict, Any
from backend.schemas.purification import (
    DecayPoint,
    PurificationSimulationRequest,
    PurificationSimulationResponse,
)

ASSUMPTIONS_LEDGER = [
    "Instantaneous and perfect spatial mixing throughout the room volume (no dead zones or localized concentration gradients).",
    "Zero continuing indoor emission sources (no cooking, smoking, incense, or dust resuspension).",
    "Zero building envelope infiltration/exfiltration through doors, windows, and cracks (ACH_nat = 0).",
    "Zero natural particle deposition, gravitational settling, or wall adsorption losses.",
    "Continuous operation at rated Clean Air Delivery Rate (CADR) with a clean filter and zero bypass."
]


def simulate_purification(
    room_area_m2: float = 20.0,
    ceiling_height_m: float = 2.8,
    initial_pm25_ug_m3: float = 67.7,
    cadr_m3_h: float = 300.0,
    runtime_hours: float = 2.0
) -> PurificationSimulationResponse:
    """
    Computes idealized first-order room PM2.5 decay and generates a 40-point decay curve.
    """
    # Validation
    if room_area_m2 <= 0 or ceiling_height_m <= 0:
        raise ValueError("Room dimensions must be strictly positive.")
    if initial_pm25_ug_m3 < 0:
        raise ValueError("Initial PM2.5 concentration cannot be negative.")
    if cadr_m3_h < 0:
        raise ValueError("CADR cannot be negative.")
    if runtime_hours < 0:
        raise ValueError("Runtime duration cannot be negative.")

    a = float(room_area_m2)
    h = float(ceiling_height_m)
    c0 = float(initial_pm25_ug_m3)
    cadr = float(cadr_m3_h)
    t = float(runtime_hours)

    volume = round(a * h, 2)
    ach_cadr = round(cadr / volume, 2) if volume > 0 else 0.0

    # Boundary handling: CADR = 0 or t = 0
    if cadr == 0.0 or t == 0.0 or volume == 0.0:
        final_pm25 = c0
        reduction_pct = 0.0
    else:
        # C(t) = C0 * exp(-(CADR / V) * t)
        decay_factor = math.exp(-(cadr / volume) * t)
        final_pm25 = round(c0 * decay_factor, 2)
        reduction_pct = round((1.0 - (final_pm25 / c0)) * 100.0, 1) if c0 > 0 else 0.0

    # 40-point decay curve generation
    num_points = 40
    decay_curve: List[DecayPoint] = []

    for i in range(num_points):
        ti = (t * i / (num_points - 1)) if (num_points > 1 and t > 0) else 0.0
        if cadr == 0.0 or volume == 0.0 or ti == 0.0:
            c_ti = c0
            red_ti = 0.0
        else:
            c_ti = round(c0 * math.exp(-(cadr / volume) * ti), 2)
            red_ti = round((1.0 - (c_ti / c0)) * 100.0, 1) if c0 > 0 else 0.0

        decay_curve.append(
            DecayPoint(
                time_hours=round(ti, 3),
                pm25_ug_m3=c_ti,
                reduction_pct=red_ti
            )
        )

    return PurificationSimulationResponse(
        status="success",
        room_area_m2=a,
        ceiling_height_m=h,
        room_volume_m3=volume,
        initial_pm25_ug_m3=c0,
        initial_pm25_source="Initialized from outdoor city composite observation (2024-10-31) in the absence of indoor sensors. User-adjustable.",
        cadr_m3_h=cadr,
        runtime_hours=t,
        air_changes_per_hour_cadr=ach_cadr,
        final_pm25_ug_m3=final_pm25,
        percentage_reduction=reduction_pct,
        decay_curve=decay_curve,
        formula_used="C(t) = C0 * exp(-(CADR / V) * t)",
        assumptions_ledger=ASSUMPTIONS_LEDGER,
        disclaimer="Theoretical first-order mass-balance scenario. Not an indoor sensor reading, not an AI prediction, and not a measured purifier test."
    )
