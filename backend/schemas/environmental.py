"""
BreatheWise Pydantic v2 validation contracts for Environmental Insights.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class StationMetadataItem(BaseModel):
    id: str = Field(..., description="Station ID or 'city_composite'")
    name: str = Field(..., description="Human-readable station name")
    active_stations_count: Optional[int] = Field(None, description="Active stations contributing to composite")
    latitude: Optional[float] = Field(None, description="Station latitude")
    longitude: Optional[float] = Field(None, description="Station longitude")
    is_active: bool = Field(True, description="True if station was active during 2023–2024 monitoring window")
    status: Optional[str] = Field(None, description="Status string (e.g. 'active', 'decommissioned')")
    message: Optional[str] = Field(None, description="Informational message for special station conditions")


class AQISummaryItem(BaseModel):
    aqi: Optional[int] = Field(None, description="CPCB Air Quality Index (null if insufficient criteria pollutants)")
    category: str = Field(..., description="CPCB 6-tier health category (Good, Satisfactory, Moderate, etc.)")
    prominent_pollutant: Optional[str] = Field(None, description="Prominent criteria pollutant driving the AQI")
    category_meta: Optional[Dict[str, Any]] = Field(None, description="Category visual metadata (color, badge, desc)")


class PollutantStatusItem(BaseModel):
    name: str = Field(..., description="Standardized pollutant key: PM2.5, PM10, NO2, SO2, CO, O3, NH3, Pb")
    display_name: str = Field(..., description="Formatted display name with chemical subscripts (e.g., PM₂.₅)")
    concentration: Optional[float] = Field(None, description="Observed concentration value (null if missing or unavailable)")
    unit: str = Field(..., description="Physical concentration unit (µg/m³ or mg/m³)")
    averaging_period: str = Field(..., description="Averaging period (e.g. '24-hour', '24-hour arithmetic daily mean', 'Not monitored')")
    sub_index: Optional[float] = Field(None, description="Official CPCB sub-index (strictly null for 24h CO/O3 and Pb)")
    tier: str = Field(..., description="CPCB tier name, 'CPCB 8h standard only', or 'Not available in supplied dataset'")
    is_valid: bool = Field(..., description="True if valid for regulatory daily AQI determination")
    is_informational: bool = Field(False, description="True if provided for informational context only")
    notes: Optional[str] = Field(None, description="Explanatory notes on regulatory validity or sensor availability")


class MeteorologyContextItem(BaseModel):
    temperature_mean: Optional[float] = Field(None, description="24h mean temperature (°C)")
    temp_min: Optional[float] = Field(None, description="Daily minimum temperature (°C)")
    temp_max: Optional[float] = Field(None, description="Daily maximum temperature (°C)")
    humidity_mean: Optional[float] = Field(None, description="24h mean relative humidity (%)")
    wind_speed_resultant: Optional[float] = Field(None, description="Resultant wind speed (km/h)")
    wind_dir_resultant: Optional[float] = Field(None, description="Resultant wind direction (degrees clockwise from North)")
    wind_u: Optional[float] = Field(None, description="Zonal wind vector component u (km/h)")
    wind_v: Optional[float] = Field(None, description="Meridional wind vector component v (km/h)")
    precipitation_sum: Optional[float] = Field(None, description="Total daily precipitation (mm)")
    pressure_mean: Optional[float] = Field(None, description="24h mean surface atmospheric pressure (hPa)")


class CorrelationItem(BaseModel):
    metric_x: str = Field(..., description="First environmental metric")
    metric_y: str = Field(..., description="Second environmental metric")
    pearson_r: float = Field(..., description="Pearson linear correlation coefficient")
    spearman_rho: float = Field(..., description="Spearman rank correlation coefficient")
    n_samples: int = Field(..., description="Exact count of valid observation pairs evaluated")
    p_value: Optional[float] = Field(None, description="Two-tailed p-value")
    scope: str = Field("citywide_historical", description="Statistical scope: 'citywide_historical' or 'station_specific'")
    scope_note: Optional[str] = Field(None, description="Explicit note clarifying whether correlations represent citywide composite or station-specific observations")
    description: str = Field(..., description="Retrospective non-causal observational description")


class EnvironmentalInsightsResponse(BaseModel):
    status: str = Field("success", description="API response status")
    date: str = Field(..., description="Observation date (YYYY-MM-DD)")
    is_historical: bool = Field(True, description="Always true; historical record Jan 1, 2023 to Oct 31, 2024")
    station: StationMetadataItem
    aqi_summary: AQISummaryItem
    pollutants: List[PollutantStatusItem]
    meteorology: MeteorologyContextItem
    correlation_scope: str = Field(
        "citywide_historical",
        description="Scope of the correlation matrix: 'citywide_historical', 'station_specific', or 'omitted'"
    )
    correlations: List[CorrelationItem] = Field(
        default_factory=list,
        description="List of correlation items (omitted for decommissioned stations to prevent scope confusion)"
    )
    data_integrity: Dict[str, Any] = Field(default_factory=dict, description="Audit and missingness metadata")
    disclaimer: str = Field(
        "Retrospective observational data from CPCB/CAAQM and Open-Meteo ERA5 reanalysis. "
        "Descriptive correlation does not imply causation.",
        description="Mandatory scientific non-causal disclaimer"
    )
