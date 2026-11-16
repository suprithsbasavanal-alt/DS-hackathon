"""
BreatheWise - Pollutant Threshold Engine & CPCB Table 3.2 Adapter
Authoritative reference: Central Pollution Control Board (CPCB) Technical Report (October 2014), Table 3.2.

This module acts as a strict, typed adapter to backend.cpcb_calculator:
1. Validates physical units (ug/m3 for particulates/gases, mg/m3 for CO).
2. Enforces CPCB Table 3.2 averaging period boundaries:
   - Daily 24h arithmetic daily means for CO and O3 return sub_index: null, tier: "CPCB 8h standard only",
     is_valid: false, is_informational: true.
   - Hourly rolling 8h metrics (available for BTM Layout & Peenya landmarks) compute official 8h sub-indices.
3. Explicit Lead (Pb) transparency:
   - Pb is unmonitored in the Bengaluru CAAQM dataset. Returns concentration: null, sub_index: null,
     tier: "Not available in supplied dataset", is_valid: false. Never represented as zero or imputed.
4. Preserves all frozen CPCB calculation logic without duplicating breakpoint tables.
"""

from typing import Dict, List, Optional, Any
from backend.cpcb_calculator import (
    calculate_subindex_official_cpcb,
    get_aqi_category,
    OFFICIAL_CLOSED_BREAKPOINTS,
    OFFICIAL_SEVERE_LOWER_THRESHOLDS,
)
from backend.schemas.environmental import PollutantStatusItem

# Standard physical units per CPCB Table 3.2 specifications
POLLUTANT_STANDARD_UNITS: Dict[str, str] = {
    "PM2.5": "µg/m³",
    "PM10": "µg/m³",
    "NO2": "µg/m³",
    "SO2": "µg/m³",
    "CO": "mg/m³",
    "O3": "µg/m³",
    "NH3": "µg/m³",
    "Pb": "µg/m³",
}

# Display names with standard chemical formatting
POLLUTANT_DISPLAY_NAMES: Dict[str, str] = {
    "PM2.5": "PM₂.₅",
    "PM10": "PM₁₀",
    "NO2": "NO₂",
    "SO2": "SO₂",
    "CO": "CO",
    "O3": "Ozone (O₃)",
    "NH3": "Ammonia (NH₃)",
    "Pb": "Lead (Pb)",
}

# Key mapping from various dataset formats to standard pollutant names
KEY_TO_STANDARD_NAME: Dict[str, str] = {
    "pm25": "PM2.5",
    "pm2.5": "PM2.5",
    "PM2.5": "PM2.5",
    "pm10": "PM10",
    "PM10": "PM10",
    "no2": "NO2",
    "NO2": "NO2",
    "so2": "SO2",
    "SO2": "SO2",
    "co": "CO",
    "CO": "CO",
    "o3": "O3",
    "ozone": "O3",
    "Ozone": "O3",
    "O3": "O3",
    "nh3": "NH3",
    "NH3": "NH3",
    "pb": "Pb",
    "Pb": "Pb",
}


def evaluate_single_pollutant(
    pollutant_key: str,
    concentration: Optional[float],
    unit: Optional[str] = None,
    is_daily: bool = True
) -> PollutantStatusItem:
    """
    Evaluates a single criteria pollutant against CPCB Table 3.2 regulatory standards.

    Parameters:
    - pollutant_key: Raw key, e.g. 'pm25', 'PM2.5', 'co', 'CO', 'pb'
    - concentration: Observed numeric concentration (None if unmonitored or missing)
    - unit: Optional unit string for verification (raises ValueError if mismatched)
    - is_daily: True if concentration is derived from a 24-hour daily composite

    Returns:
    - PollutantStatusItem validation schema object
    """
    std_name = KEY_TO_STANDARD_NAME.get(pollutant_key)
    if not std_name:
        raise ValueError(f"Unsupported pollutant key: '{pollutant_key}'")

    expected_unit = POLLUTANT_STANDARD_UNITS[std_name]
    if unit is not None and unit.strip().lower() != expected_unit.strip().lower():
        # Handle unicode micro character difference (u vs µ)
        clean_unit = unit.strip().replace("ug", "µg").replace("uG", "µg")
        if clean_unit != expected_unit:
            raise ValueError(
                f"Unit mismatch for {std_name}: expected '{expected_unit}', received '{unit}'"
            )

    display_name = POLLUTANT_DISPLAY_NAMES[std_name]

    # 1. Lead (Pb) Transparency
    if std_name == "Pb":
        return PollutantStatusItem(
            name="Pb",
            display_name=display_name,
            concentration=None,
            unit=expected_unit,
            averaging_period="Not monitored",
            sub_index=None,
            tier="Not available in supplied dataset",
            is_valid=False,
            is_informational=False,
            notes="Lead (Pb) is not monitored in the supplied Bengaluru CAAQM dataset."
        )

    # 2. Missing or sensor glitch concentration
    if concentration is None:
        return PollutantStatusItem(
            name=std_name,
            display_name=display_name,
            concentration=None,
            unit=expected_unit,
            averaging_period="24-hour" if is_daily else "Hourly / 8-hour",
            sub_index=None,
            tier="Missing Data",
            is_valid=False,
            is_informational=False,
            notes=f"No valid observations recorded for {std_name}."
        )

    c = float(concentration)

    # Reject physical impossibility / negative sensor readings
    if c < 0:
        return PollutantStatusItem(
            name=std_name,
            display_name=display_name,
            concentration=c,
            unit=expected_unit,
            averaging_period="24-hour" if is_daily else "Hourly / 8-hour",
            sub_index=None,
            tier="Invalid (Sensor Glitch)",
            is_valid=False,
            is_informational=False,
            notes="Negative concentration rejected per CPCB data-validation guidelines."
        )

    # 3. Daily CO and O3 Protocol: CPCB Table 3.2 specifies standards for 8-hour averages ONLY
    if is_daily and std_name in ("CO", "O3"):
        return PollutantStatusItem(
            name=std_name,
            display_name=display_name,
            concentration=round(c, 2),
            unit=expected_unit,
            averaging_period="24-hour arithmetic daily mean",
            sub_index=None,
            tier="CPCB 8h standard only",
            is_valid=False,
            is_informational=True,
            notes=(
                f"CPCB Table 3.2 prescribes {std_name} standards for 8-hour averages only. "
                f"Regulatory sub-index cannot be computed from 24-hour daily composite averages."
            )
        )

    # 4. Standard 24h Criteria Pollutants (PM2.5, PM10, NO2, SO2, NH3) or true 8h CO/O3
    averaging_period = "8-hour" if std_name in ("CO", "O3") else "24-hour"
    sub_index = calculate_subindex_official_cpcb(std_name, c)
    tier = get_aqi_category(sub_index) if sub_index is not None else "Unknown"

    return PollutantStatusItem(
        name=std_name,
        display_name=display_name,
        concentration=round(c, 2),
        unit=expected_unit,
        averaging_period=averaging_period,
        sub_index=sub_index,
        tier=tier,
        is_valid=True,
        is_informational=False,
        notes=None
    )


def evaluate_all_criteria_pollutants(
    pollutant_data: Dict[str, Any],
    is_daily: bool = True
) -> List[PollutantStatusItem]:
    """
    Evaluates all 7 criteria pollutants plus Pb in canonical CPCB order:
    [PM2.5, PM10, NO2, SO2, CO, O3, NH3, Pb]
    """
    canonical_order = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "NH3", "Pb"]
    items = []

    for std_name in canonical_order:
        val = None
        # Check standard name and lowercase alternatives
        for k, v in pollutant_data.items():
            if KEY_TO_STANDARD_NAME.get(k) == std_name:
                val = v
                break

        item = evaluate_single_pollutant(
            pollutant_key=std_name,
            concentration=val,
            unit=POLLUTANT_STANDARD_UNITS[std_name],
            is_daily=is_daily
        )
        items.append(item)

    return items
