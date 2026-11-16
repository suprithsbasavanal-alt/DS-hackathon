"""
BreatheWise - CPCB Official IND-AQI Calculation Engine
Authoritative Reference: Central Pollution Control Board (CPCB) Technical Report (October 2014), Table 3.2.

Mathematical Formulation:
1. For Categories 1 to 5 (Good, Satisfactory, Moderate, Poor, Very Poor):
   Sub-index Ip = [(I_HI - I_LO) / (B_HI - B_LO)] * (Cp - B_LO) + I_LO
   where:
   - Cp: Pollutant concentration
   - B_LO, B_HI: Lower and upper concentration breakpoints
   - I_LO, I_HI: Lower and upper sub-index breakpoints

2. Category 6 (Severe, 401 - 500):
   Project Implementation Policy: Severe values reported at the 500 ceiling cap.
   Note: CPCB 2014 Table 3.2 specifies open-ended lower concentration thresholds
   (e.g., PM2.5 > 250 ug/m3, PM10 > 430 ug/m3) without publishing upper concentration limits (B_HI).
   CPCB guidelines provide linear interpolation for categories 1-5, but do not prescribe an official
   interpolation formula beyond the Severe lower boundary.
   In BreatheWise, assigning 500.0 is an explicit project implementation policy reflecting
   the national index ceiling, NOT an officially prescribed CPCB linear interpolation formula.
   Sensor readings exceeding analyzer physical limits (> 1000 ug/m3) are logged as sensor saturation faults.

3. Station Overall AQI & Prominent Pollutant:
   Station AQI = max_p (Ip)
   Prominent Pollutant = argmax_p (Ip)
   Minimum Criteria: >= 3 valid criteria sub-indices, of which >= 1 must be PM2.5 or PM10.
   CO and O3 Protocol: Excluded from daily station AQI calculations when derived from 24-hour daily means.
"""

from typing import Dict, Optional, Tuple, Any

# Official CPCB 2014 Table 3.2 Breakpoints for Categories 1 to 5
# Format: (B_LO, B_HI, I_LO, I_HI)
OFFICIAL_CLOSED_BREAKPOINTS: Dict[str, list] = {
    "PM10": [
        (0.0, 50.0, 0, 50),        # Good
        (50.0, 100.0, 51, 100),    # Satisfactory
        (100.0, 250.0, 101, 200),  # Moderate
        (250.0, 350.0, 201, 300),  # Poor
        (350.0, 430.0, 301, 400),  # Very Poor
    ],
    "PM2.5": [
        (0.0, 30.0, 0, 50),
        (30.0, 60.0, 51, 100),
        (60.0, 90.0, 101, 200),
        (90.0, 120.0, 201, 300),
        (120.0, 250.0, 301, 400),
    ],
    "NO2": [
        (0.0, 40.0, 0, 50),
        (40.0, 80.0, 51, 100),
        (80.0, 180.0, 101, 200),
        (180.0, 280.0, 201, 300),
        (280.0, 400.0, 301, 400),
    ],
    "SO2": [
        (0.0, 40.0, 0, 50),
        (40.0, 80.0, 51, 100),
        (80.0, 380.0, 101, 200),
        (380.0, 800.0, 201, 300),
        (800.0, 1600.0, 301, 400),
    ],
    "CO": [  # 8-hourly average, mg/m3
        (0.0, 1.0, 0, 50),
        (1.0, 2.0, 51, 100),
        (2.0, 10.0, 101, 200),
        (10.0, 17.0, 201, 300),
        (17.0, 34.0, 301, 400),
    ],
    "O3": [  # 8-hourly average, ug/m3
        (0.0, 50.0, 0, 50),
        (50.0, 100.0, 51, 100),
        (100.0, 168.0, 101, 200),
        (168.0, 208.0, 201, 300),
        (208.0, 748.0, 301, 400),
    ],
    "NH3": [
        (0.0, 200.0, 0, 50),
        (200.0, 400.0, 51, 100),
        (400.0, 800.0, 101, 200),
        (800.0, 1200.0, 201, 300),
        (1200.0, 1800.0, 301, 400),
    ],
    "Pb": [
        (0.0, 0.5, 0, 50),
        (0.5, 1.0, 51, 100),
        (1.0, 2.0, 101, 200),
        (2.0, 3.0, 201, 300),
        (3.0, 3.5, 301, 400),
    ],
}

# Official CPCB 2014 Table 3.2 Lower Concentration Thresholds for Category 6 (Severe)
OFFICIAL_SEVERE_LOWER_THRESHOLDS: Dict[str, float] = {
    "PM10": 430.0,
    "PM2.5": 250.0,
    "NO2": 400.0,
    "SO2": 1600.0,
    "CO": 34.0,
    "O3": 748.0,
    "NH3": 1800.0,
    "Pb": 3.5,
}

# Standard CPCB 6-tier Health Categories & Visual Colors
CPCB_CATEGORIES = [
    {"name": "Good", "min": 0, "max": 50, "color": "#10B981", "badge": "bg-emerald-500/10 text-emerald-600 border-emerald-500/20", "desc": "Minimal impact."},
    {"name": "Satisfactory", "min": 51, "max": 100, "color": "#84CC16", "badge": "bg-lime-500/10 text-lime-600 border-lime-500/20", "desc": "Minor breathing discomfort to sensitive people."},
    {"name": "Moderate", "min": 101, "max": 200, "color": "#EAB308", "badge": "bg-amber-500/10 text-amber-600 border-amber-500/20", "desc": "Breathing discomfort to people with lungs, asthma and heart diseases."},
    {"name": "Poor", "min": 201, "max": 300, "color": "#F97316", "badge": "bg-orange-500/10 text-orange-600 border-orange-500/20", "desc": "Breathing discomfort to most people on prolonged exposure."},
    {"name": "Very Poor", "min": 301, "max": 400, "color": "#EF4444", "badge": "bg-red-500/10 text-red-600 border-red-500/20", "desc": "Respiratory illness on prolonged exposure."},
    {"name": "Severe", "min": 401, "max": 500, "color": "#991B1B", "badge": "bg-rose-950/20 text-rose-500 border-rose-500/30", "desc": "Affects healthy people and seriously impacts those with existing diseases."},
]


def calculate_subindex_official_cpcb(pollutant: str, concentration: Optional[float]) -> Optional[float]:
    """
    Computes pollutant sub-index Ip adhering to official CPCB 2014 Table 3.2 rules:
    - Piecewise linear interpolation on closed brackets 1-5 (Good to Very Poor).
    - For open-ended Severe range (Cp > B_LO_severe):
      Project Implementation Policy: Severe values reported at the 500 ceiling cap.
      Note: CPCB Table 3.2 specifies the Severe category (401-500) with an open-ended
      lower threshold (e.g. PM2.5 > 250) but does not prescribe an interpolation formula
      beyond that boundary. In BreatheWise, assigning 500 is an explicit project implementation
      policy reflecting the official 500 index ceiling, NOT an officially prescribed CPCB
      interpolation formula.
    - Rejects negative inputs (sensor glitch) by returning None.
    """
    if concentration is None or concentration < 0:
        return None
        
    c = float(concentration)
    if pollutant not in OFFICIAL_CLOSED_BREAKPOINTS:
        raise ValueError(f"Unsupported criteria pollutant: {pollutant}")
        
    table = OFFICIAL_CLOSED_BREAKPOINTS[pollutant]
    
    # 1. Piecewise linear interpolation on closed categories 1-5
    for b_lo, b_hi, i_lo, i_hi in table:
        if b_lo <= c <= b_hi:
            sub = i_lo + ((i_hi - i_lo) / (b_hi - b_lo)) * (c - b_lo)
            return round(sub, 1)
            
    # 2. Severe range handling (Project implementation policy: Severe values reported at 500 ceiling)
    severe_threshold = OFFICIAL_SEVERE_LOWER_THRESHOLDS[pollutant]
    if c > severe_threshold:
        return 500.0
        
    return 0.0


def get_aqi_category(sub_index: Optional[float]) -> str:
    """Maps sub-index or station AQI to official CPCB 6-tier health category string."""
    if sub_index is None:
        return "Unknown"
    val = round(sub_index)
    if val <= 50:
        return "Good"
    elif val <= 100:
        return "Satisfactory"
    elif val <= 200:
        return "Moderate"
    elif val <= 300:
        return "Poor"
    elif val <= 400:
        return "Very Poor"
    else:
        return "Severe"


def get_aqi_category_meta(sub_index: Optional[float]) -> Dict[str, Any]:
    """Returns rich metadata (name, color, badge, description) for an AQI value."""
    category_name = get_aqi_category(sub_index)
    for cat in CPCB_CATEGORIES:
        if cat["name"] == category_name:
            return cat
    return {
        "name": "Unknown",
        "min": 0,
        "max": 0,
        "color": "#94A3B8",
        "badge": "bg-slate-500/10 text-slate-500 border-slate-500/20",
        "desc": "Insufficient data.",
    }


def calculate_station_aqi(
    pollutants_dict: Dict[str, Optional[float]],
    exclude_co_o3_daily: bool = True
) -> Tuple[Optional[int], Optional[str], Dict[str, float]]:
    """
    Computes station overall AQI, prominent pollutant, and criteria sub-indices:
    
    CPCB Regulatory Constraints Enforced:
    1. Exclusion of CO/O3: When evaluate_daily=True, CO and O3 are excluded from daily station AQI
       because 24-hour daily means cannot substitute for CPCB 8-hour metrics.
    2. Minimum Criteria: At least 3 valid criteria sub-indices must be present.
    3. Particulate Requirement: At least one particulate matter (PM2.5 or PM10) must be present.
    4. Worst-Pollutant Principle: Station AQI = max_p (Ip). Prominent = argmax_p (Ip).
    
    Returns:
    (station_aqi, prominent_pollutant, sub_indices_dict)
    If constraints are not satisfied, returns (None, None, sub_indices_dict).
    """
    sub_indices: Dict[str, float] = {}
    
    # Filter candidate pollutants
    candidates = {}
    for p, val in pollutants_dict.items():
        if exclude_co_o3_daily and p in ("CO", "O3", "Ozone"):
            continue
        # Normalize naming
        std_p = "O3" if p == "Ozone" else p
        if val is not None and val >= 0:
            candidates[std_p] = val

    # Must contain at least one particulate matter
    has_particulate = "PM2.5" in candidates or "PM10" in candidates
    if not has_particulate:
        return None, None, {}
        
    for p, val in candidates.items():
        if p in OFFICIAL_CLOSED_BREAKPOINTS:
            sub = calculate_subindex_official_cpcb(p, val)
            if sub is not None:
                sub_indices[p] = sub

    # Minimum 3 criteria pollutants requirement
    if len(sub_indices) < 3:
        return None, None, sub_indices

    # Worst-pollutant principle
    prominent = max(sub_indices, key=lambda k: sub_indices[k])
    station_aqi = int(round(sub_indices[prominent]))
    
    return station_aqi, prominent, sub_indices
