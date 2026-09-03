from typing import Dict, List


# Prototype weights
CARBON_WEIGHT = 0.35
ENERGY_WEIGHT = 0.30
COST_WEIGHT = 0.20
COMFORT_WEIGHT = 0.15


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def normalize(value: float, maximum: float) -> float:
    if maximum <= 0:
        return 0.0

    return clamp(value / maximum, 0.0, 1.0)


def calculate_action_score(
    energy_benefit: float,
    carbon_benefit: float,
    cost_benefit: float,
    comfort_score: float,
) -> float:

    score = (
        carbon_benefit * CARBON_WEIGHT
        + energy_benefit * ENERGY_WEIGHT
        + cost_benefit * COST_WEIGHT
        + comfort_score * COMFORT_WEIGHT
    )

    return round(score * 100, 2)


def optimize_energy(
    occupancy_percent: float,
    temperature_c: float,
    daylight_level: float,
    current_energy_kwh: float,
    flexible_load_kwh: float,
    grid_carbon_intensity: float,
) -> List[Dict]:

    actions = []

    # ---------------------------------------------------------
    # ACTION 1: Reduce lighting
    # ---------------------------------------------------------

    lighting_saving = 0.0

    if daylight_level >= 60 and occupancy_percent <= 70:
        lighting_saving = current_energy_kwh * 0.10

    lighting_carbon = (
        lighting_saving * grid_carbon_intensity / 1000
    )

    lighting_energy_score = normalize(
        lighting_saving,
        current_energy_kwh * 0.15
    )

    lighting_carbon_score = normalize(
        lighting_carbon,
        current_energy_kwh * grid_carbon_intensity / 1000 * 0.15
    )

    lighting_cost_score = lighting_energy_score

    lighting_comfort = 0.85 if occupancy_percent <= 70 else 0.55

    lighting_score = calculate_action_score(
        lighting_energy_score,
        lighting_carbon_score,
        lighting_cost_score,
        lighting_comfort,
    )

    actions.append({
        "action": "Reduce lighting load",
        "score": lighting_score,
        "energy_saving_kwh": round(lighting_saving, 2),
        "cost_saving_inr": round(lighting_saving * 8, 2),
        "carbon_reduction_kg": round(lighting_carbon, 2),
        "comfort_impact": "Low",
        "reason": (
            "High daylight and moderate occupancy make lighting "
            "reduction a suitable low-impact action."
        ),
    })

    # ---------------------------------------------------------
    # ACTION 2: Adjust HVAC setpoint
    # ---------------------------------------------------------

    hvac_saving = 0.0

    if temperature_c >= 27 and occupancy_percent <= 80:
        hvac_saving = current_energy_kwh * 0.08

    hvac_carbon = (
        hvac_saving * grid_carbon_intensity / 1000
    )

    hvac_energy_score = normalize(
        hvac_saving,
        current_energy_kwh * 0.12
    )

    hvac_carbon_score = normalize(
        hvac_carbon,
        current_energy_kwh * grid_carbon_intensity / 1000 * 0.12
    )

    hvac_cost_score = hvac_energy_score

    hvac_comfort = 0.65

    hvac_score = calculate_action_score(
        hvac_energy_score,
        hvac_carbon_score,
        hvac_cost_score,
        hvac_comfort,
    )

    actions.append({
        "action": "Adjust HVAC setpoint by 1°C",
        "score": hvac_score,
        "energy_saving_kwh": round(hvac_saving, 2),
        "cost_saving_inr": round(hvac_saving * 8, 2),
        "carbon_reduction_kg": round(hvac_carbon, 2),
        "comfort_impact": "Moderate",
        "reason": (
            "Temperature conditions indicate an opportunity "
            "for a small HVAC adjustment."
        ),
    })

    # ---------------------------------------------------------
    # ACTION 3: Shift flexible load
    # ---------------------------------------------------------

    load_saving = 0.0

    if flexible_load_kwh > 0 and grid_carbon_intensity >= 400:
        load_saving = flexible_load_kwh * 0.15

    load_carbon = (
        load_saving * grid_carbon_intensity / 1000
    )

    load_energy_score = normalize(
        load_saving,
        max(flexible_load_kwh * 0.20, 0.01)
    )

    load_carbon_score = normalize(
        load_carbon,
        max(
            flexible_load_kwh * grid_carbon_intensity / 1000 * 0.20,
            0.01,
        )
    )

    load_cost_score = load_energy_score

    load_comfort = 0.95

    load_score = calculate_action_score(
        load_energy_score,
        load_carbon_score,
        load_cost_score,
        load_comfort,
    )

    actions.append({
        "action": "Shift flexible load",
        "score": load_score,
        "energy_saving_kwh": round(load_saving, 2),
        "cost_saving_inr": round(load_saving * 8, 2),
        "carbon_reduction_kg": round(load_carbon, 2),
        "comfort_impact": "Very Low",
        "reason": (
            "High grid carbon intensity makes shifting flexible "
            "loads potentially beneficial."
        ),
    })

    # ---------------------------------------------------------
    # ACTION 4: No change
    # ---------------------------------------------------------

    actions.append({
        "action": "No change",
        "score": 15.0,
        "energy_saving_kwh": 0.0,
        "cost_saving_inr": 0.0,
        "carbon_reduction_kg": 0.0,
        "comfort_impact": "None",
        "reason": (
            "Maintain current operation when optimization benefits "
            "are insufficient."
        ),
    })

    # Highest score first
    actions.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return actions
