"""
BreatheWise - Deterministic Health Advisory Rule Engine
Authoritative Reference: Central Pollution Control Board (CPCB) Table 3.2 Health Guidance.

Features:
1. Deterministic mapping from CPCB AQI categories to authoritative rule IDs.
2. Pollutant-specific threshold alert rules (PM2.5 > 60, PM10 > 100, NO2 > 40).
3. Structured guidance for the general public and sensitive cohorts (asthma, elderly/children, outdoor workers).
4. Full trigger transparency: records the exact metric and threshold condition.
5. Strict non-medical disclaimer on all outputs. Zero fabricated health claims.
"""

from typing import Dict, List, Optional, Any
from backend.cpcb_calculator import get_aqi_category
from backend.schemas.health import (
    SensitiveGroupAdvice,
    TriggeredAdvisoryItem,
    HealthAdvisoryResponse,
)

AQI_CATEGORY_RULES = {
    "Good": {
        "rule_id": "RULE-AQI-GOOD-01",
        "category": "Good (0–50)",
        "general_public": "Air quality is considered satisfactory, and air pollution poses little or no health risk. Enjoy outdoor activities freely.",
        "sensitive": SensitiveGroupAdvice(
            asthma="Normal outdoor routines permitted; negligible irritation risk.",
            elderly_and_children="Ideal conditions for outdoor play, school activities, and walks.",
            outdoor_workers="No protective respiratory equipment required under current ambient air conditions."
        ),
        "outdoor_activity": "Ideal conditions for outdoor sports, distance running, cycling, and general physical exertion."
    },
    "Satisfactory": {
        "rule_id": "RULE-AQI-SAT-01",
        "category": "Satisfactory (51–100)",
        "general_public": "Air quality is acceptable for healthy individuals. Minor breathing discomfort may occur in unusually sensitive people.",
        "sensitive": SensitiveGroupAdvice(
            asthma="Individuals with severe asthma should observe personal tolerance during high-intensity exertion.",
            elderly_and_children="Normal activities permitted; customary hydration and rest breaks recommended.",
            outdoor_workers="Standard operational routines permitted without environmental restrictions."
        ),
        "outdoor_activity": "Outdoor sports and workouts permitted; observe standard warm-ups and hydration."
    },
    "Moderate": {
        "rule_id": "RULE-AQI-MOD-01",
        "category": "Moderate (101–200)",
        "general_public": "May cause breathing discomfort to people with lungs, asthma, and heart diseases. Healthy individuals may experience slight throat irritation during prolonged exertion.",
        "sensitive": SensitiveGroupAdvice(
            asthma="Keep prescribed rescue inhalers accessible. Take frequent rest breaks if coughing or shortness of breath develops.",
            elderly_and_children="Limit prolonged high-exertion outdoor play; prefer shaded or indoor recreational alternatives during midday.",
            outdoor_workers="Take scheduled rest breaks away from heavy vehicular traffic corridors."
        ),
        "outdoor_activity": "Reduce the duration and intensity of outdoor workouts. Avoid exercising adjacent to congested arterial roads."
    },
    "Poor": {
        "rule_id": "RULE-AQI-POOR-01",
        "category": "Poor (201–300)",
        "general_public": "Breathing discomfort to most people on prolonged exposure. Avoid prolonged outdoor physical exertion.",
        "sensitive": SensitiveGroupAdvice(
            asthma="Remain indoors in well-sealed rooms; avoid any strenuous outdoor exertion. Monitor peak flow readings if prescribed.",
            elderly_and_children="Children and senior citizens should remain indoors. Keep windows closed during peak traffic hours.",
            outdoor_workers="Wear a certified well-fitted particulate respirator (N95/FFP2). Rotate shifts to reduce total exposure."
        ),
        "outdoor_activity": "Avoid outdoor running, cycling, and intense field sports. Substitute with indoor cardiovascular workouts."
    },
    "Very Poor": {
        "rule_id": "RULE-AQI-VPOOR-01",
        "category": "Very Poor (301–400)",
        "general_public": "Respiratory illness to the people on prolonged exposure. Significantly reduce all outdoor activities. Keep home and workplace windows closed.",
        "sensitive": SensitiveGroupAdvice(
            asthma="Strictly avoid outdoor exposure. Consult your physician if experiencing persistent wheezing or breathlessness.",
            elderly_and_children="Vulnerable groups must remain strictly indoors. Use mechanical or HEPA air filtration if available.",
            outdoor_workers="Mandatory certified particulate respirator usage. Halt non-essential heavy manual labor outdoors."
        ),
        "outdoor_activity": "Prohibit outdoor physical training, sports events, and morning walks."
    },
    "Severe": {
        "rule_id": "RULE-AQI-SEV-01",
        "category": "Severe (401–500)",
        "general_public": "Affects healthy people and seriously impacts those with existing diseases. Emergency environmental conditions. Avoid all outdoor activity.",
        "sensitive": SensitiveGroupAdvice(
            asthma="Emergency hazard. Remain in a designated clean room with continuous air filtration. Seek prompt medical care if distress occurs.",
            elderly_and_children="Strict total indoor confinement. Avoid any external ventilation intake.",
            outdoor_workers="All non-emergency outdoor manual labor must be suspended."
        ),
        "outdoor_activity": "Complete suspension of all outdoor exercise and public gatherings."
    }
}


def evaluate_health_advisories(
    aqi: float,
    pollutants: Optional[Dict[str, Optional[float]]] = None,
    evaluation_date: Optional[str] = None,
    station_id: Optional[str] = None,
    prominent_pollutant: Optional[str] = None,
    is_hypothetical: bool = False
) -> HealthAdvisoryResponse:
    """
    Evaluates deterministic CPCB health advisories for a given AQI and optional pollutant levels.
    """
    val = float(aqi)
    # Clamp to valid non-negative index range
    val_clamped = max(0.0, min(500.0, val))
    cat = get_aqi_category(val_clamped)

    cat_rule = AQI_CATEGORY_RULES.get(cat, AQI_CATEGORY_RULES["Moderate"])

    advisories = [
        TriggeredAdvisoryItem(
            rule_id=cat_rule["rule_id"],
            category=cat,
            trigger_metric=f"AQI: {round(val_clamped)} ({cat})",
            trigger_value=round(val_clamped, 1),
            general_public_advice=cat_rule["general_public"],
            sensitive_groups_advice=cat_rule["sensitive"],
            outdoor_activity_recommendation=cat_rule["outdoor_activity"]
        )
    ]

    # Pollutant-specific supplemental alerts
    if pollutants:
        pm25 = pollutants.get("pm25") or pollutants.get("PM2.5")
        if pm25 is not None and float(pm25) > 60.0:
            advisories.append(
                TriggeredAdvisoryItem(
                    rule_id="RULE-PM25-ELEV-01",
                    category="Fine Particulate Alert",
                    trigger_metric=f"PM2.5: {round(float(pm25), 1)} µg/m³ (Exceeds CPCB 24h standard of 60 µg/m³)",
                    trigger_value=round(float(pm25), 1),
                    general_public_advice="Fine particulate accumulation increases alveolar penetration. Wear a certified N95 mask in high-traffic or dusty areas.",
                    sensitive_groups_advice=SensitiveGroupAdvice(
                        asthma="Fine particulates penetrate deep into the lower airways; minimize outdoor time and carry prescribed inhalers.",
                        elderly_and_children="Avoid outdoor play near busy roadways during morning inversion hours.",
                        outdoor_workers="Wear particulate-filtering masks during outdoor shifts."
                    ),
                    outdoor_activity_recommendation="Avoid outdoor cardio workouts near major roadways while PM2.5 levels remain elevated."
                )
            )

        pm10 = pollutants.get("pm10") or pollutants.get("PM10")
        if pm10 is not None and float(pm10) > 100.0:
            advisories.append(
                TriggeredAdvisoryItem(
                    rule_id="RULE-PM10-ELEV-01",
                    category="Coarse Dust Alert",
                    trigger_metric=f"PM10: {round(float(pm10), 1)} µg/m³ (Exceeds CPCB 24h standard of 100 µg/m³)",
                    trigger_value=round(float(pm10), 1),
                    general_public_advice="Coarse road and construction dust alert. Wear eye and airway protection in active transit corridors.",
                    sensitive_groups_advice=SensitiveGroupAdvice(
                        asthma="Coarse particles trigger upper airway and conjunctival irritation; rinse eyes and mouth after outdoor exposure.",
                        elderly_and_children="Keep home windows facing major streets closed during high wind or traffic periods.",
                        outdoor_workers="Use safety eyewear and dust masks in unpaved or construction zones."
                    ),
                    outdoor_activity_recommendation="Opt for paved park trails away from vehicular traffic and construction sites."
                )
            )

        no2 = pollutants.get("no2") or pollutants.get("NO2")
        if no2 is not None and float(no2) > 40.0:
            advisories.append(
                TriggeredAdvisoryItem(
                    rule_id="RULE-NO2-RUSH-01",
                    category="Combustion / Traffic Alert",
                    trigger_metric=f"NO2: {round(float(no2), 1)} µg/m³ (Elevated vehicular combustion marker)",
                    trigger_value=round(float(no2), 1),
                    general_public_advice="Elevated nitrogen dioxide signals vehicular exhaust accumulation. Recirculate cabin air in motor vehicles.",
                    sensitive_groups_advice=SensitiveGroupAdvice(
                        asthma="NO2 increases bronchial reactivity; avoid walking along congested arterial roads during peak rush hours.",
                        elderly_and_children="Avoid prolonged waiting at street intersections or outdoor bus stands during peak traffic.",
                        outdoor_workers="Traffic police and street vendors should take breaks in well-ventilated indoor spaces."
                    ),
                    outdoor_activity_recommendation="Schedule outdoor activities outside of morning (8–10 AM) and evening (6–9 PM) rush hours."
                )
            )

    return HealthAdvisoryResponse(
        status="success",
        evaluation_date=evaluation_date,
        station_id=station_id,
        is_hypothetical=is_hypothetical,
        aqi=round(val_clamped, 1),
        category=cat,
        prominent_pollutant=prominent_pollutant,
        advisories=advisories,
        medical_disclaimer="General public health information based on CPCB guidance. Not individualized medical advice or clinical diagnosis."
    )
