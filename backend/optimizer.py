
from typing import Dict, List


# ============================================================
# ECOPILOT AI - OPTIMIZATION CONFIGURATION
# ============================================================

# Multi-objective optimization weights
CARBON_WEIGHT = 0.35
ENERGY_WEIGHT = 0.30
COST_WEIGHT = 0.20
COMFORT_WEIGHT = 0.15

# Prototype electricity tariff
ELECTRICITY_TARIFF_INR = 8.0

# Maximum expected saving used for normalization
# These are prototype assumptions and can later be
# replaced with real campus/BMS data.
LIGHTING_MAX_SAVING_FRACTION = 0.15
HVAC_MAX_SAVING_FRACTION = 0.12
FLEXIBLE_LOAD_MAX_SAVING_FRACTION = 0.20


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clamp(value: float, minimum: float, maximum: float) -> float:
    """Keep a value between minimum and maximum."""
    return max(minimum, min(value, maximum))


def normalize(value: float, maximum: float) -> float:
    """Convert a value into a 0-1 range."""
    if maximum <= 0:
        return 0.0

    return clamp(value / maximum, 0.0, 1.0)


def calculate_action_score(
    energy_benefit: float,
    carbon_benefit: float,
    cost_benefit: float,
    comfort_score: float,
) -> float:
    """
    Calculate the multi-objective score for an action.

    Higher score = better overall recommendation.
    """

    score = (
        carbon_benefit * CARBON_WEIGHT
        + energy_benefit * ENERGY_WEIGHT
        + cost_benefit * COST_WEIGHT
        + comfort_score * COMFORT_WEIGHT
    )

    return round(score * 100, 2)


def calculate_energy_reduction_percent(
    baseline_energy_kwh: float,
    energy_saving_kwh: float,
) -> float:
    """Calculate percentage reduction from baseline energy."""

    if baseline_energy_kwh <= 0:
        return 0.0

    reduction = (
        energy_saving_kwh / baseline_energy_kwh
    ) * 100

    return round(clamp(reduction, 0.0, 100.0), 2)


def calculate_confidence(actions: List[Dict]) -> float:
    """
    Estimate recommendation confidence using the difference
    between the best and second-best feasible actions.

    This is a prototype confidence indicator, not a statistical
    probability.
    """

    feasible_actions = [
        action
        for action in actions
        if action["feasible"]
    ]

    if not feasible_actions:
        return 50.0

    if len(feasible_actions) == 1:
        return 90.0

    top_score = feasible_actions[0]["score"]
    second_score = feasible_actions[1]["score"]

    score_margin = top_score - second_score

    confidence = 70 + (score_margin * 0.5)

    return round(clamp(confidence, 50.0, 95.0), 2)


# ============================================================
# MAIN OPTIMIZATION ENGINE
# ============================================================

def optimize_energy(
    occupancy_percent: float,
    temperature_c: float,
    daylight_level: float,
    current_energy_kwh: float,
    flexible_load_kwh: float,
    grid_carbon_intensity: float,
) -> List[Dict]:
    """
    Evaluate available energy optimization actions.

    The optimizer:
    1. Checks whether an action is feasible.
    2. Estimates its energy impact.
    3. Estimates cost savings.
    4. Estimates carbon reduction.
    5. Evaluates comfort impact.
    6. Calculates a weighted score.
    7. Ranks the actions.
    """

    baseline_energy = current_energy_kwh

    actions = []

    # ========================================================
    # ACTION 1 - REDUCE LIGHTING
    # ========================================================

    lighting_feasible = (
        daylight_level >= 60
        and occupancy_percent <= 70
    )

    if lighting_feasible:
        lighting_saving = (
            baseline_energy * 0.10
        )

        lighting_reason = (
            "High daylight and moderate occupancy make "
            "lighting reduction a suitable low-impact action."
        )

        lighting_comfort_score = 0.85
        lighting_comfort = "Low"

    else:
        lighting_saving = 0.0

        lighting_reason = (
            "Lighting reduction is not recommended because "
            "daylight or occupancy conditions are unsuitable."
        )

        lighting_comfort_score = 0.0
        lighting_comfort = "Not suitable"

    lighting_carbon = (
        lighting_saving
        * grid_carbon_intensity
        / 1000
    )

    lighting_cost = (
        lighting_saving
        * ELECTRICITY_TARIFF_INR
    )

    lighting_energy_score = normalize(
        lighting_saving,
        baseline_energy
        * LIGHTING_MAX_SAVING_FRACTION,
    )

    lighting_carbon_score = normalize(
        lighting_carbon,
        baseline_energy
        * grid_carbon_intensity
        / 1000
        * LIGHTING_MAX_SAVING_FRACTION,
    )

    lighting_cost_score = normalize(
        lighting_cost,
        baseline_energy
        * ELECTRICITY_TARIFF_INR
        * LIGHTING_MAX_SAVING_FRACTION,
    )

    lighting_score = (
        calculate_action_score(
            lighting_energy_score,
            lighting_carbon_score,
            lighting_cost_score,
            lighting_comfort_score,
        )
        if lighting_feasible
        else 0.0
    )

    actions.append(
        {
            "action": "Reduce lighting load",
            "feasible": lighting_feasible,
            "score": lighting_score,
            "baseline_energy_kwh": round(
                baseline_energy, 2
            ),
            "optimized_energy_kwh": round(
                baseline_energy - lighting_saving,
                2,
            ),
            "energy_saving_kwh": round(
                lighting_saving,
                2,
            ),
            "energy_reduction_percent": (
                calculate_energy_reduction_percent(
                    baseline_energy,
                    lighting_saving,
                )
            ),
            "cost_saving_inr": round(
                lighting_cost,
                2,
            ),
            "carbon_reduction_kg": round(
                lighting_carbon,
                2,
            ),
            "comfort_impact": lighting_comfort,
            "reason": lighting_reason,
        }
    )

    # ========================================================
    # ACTION 2 - ADJUST HVAC SETPOINT
    # ========================================================

    hvac_feasible = (
        temperature_c >= 27
        and occupancy_percent <= 80
    )

    if hvac_feasible:
        hvac_saving = (
            baseline_energy * 0.08
        )

        hvac_reason = (
            "Warm temperature and moderate occupancy indicate "
            "an opportunity for a small HVAC setpoint adjustment."
        )

        hvac_comfort_score = 0.65
        hvac_comfort = "Moderate"

    else:
        hvac_saving = 0.0

        hvac_reason = (
            "HVAC adjustment is not recommended because "
            "temperature or occupancy conditions are unsuitable."
        )

        hvac_comfort_score = 0.0
        hvac_comfort = "Not suitable"

    hvac_carbon = (
        hvac_saving
        * grid_carbon_intensity
        / 1000
    )

    hvac_cost = (
        hvac_saving
        * ELECTRICITY_TARIFF_INR
    )

    hvac_energy_score = normalize(
        hvac_saving,
        baseline_energy
        * HVAC_MAX_SAVING_FRACTION,
    )

    hvac_carbon_score = normalize(
        hvac_carbon,
        baseline_energy
        * grid_carbon_intensity
        / 1000
        * HVAC_MAX_SAVING_FRACTION,
    )

    hvac_cost_score = normalize(
        hvac_cost,
        baseline_energy
        * ELECTRICITY_TARIFF_INR
        * HVAC_MAX_SAVING_FRACTION,
    )

    hvac_score = (
        calculate_action_score(
            hvac_energy_score,
            hvac_carbon_score,
            hvac_cost_score,
            hvac_comfort_score,
        )
        if hvac_feasible
        else 0.0
    )

    actions.append(
        {
            "action": "Adjust HVAC setpoint by 1°C",
            "feasible": hvac_feasible,
            "score": hvac_score,
            "baseline_energy_kwh": round(
                baseline_energy,
                2,
            ),
            "optimized_energy_kwh": round(
                baseline_energy - hvac_saving,
                2,
            ),
            "energy_saving_kwh": round(
                hvac_saving,
                2,
            ),
            "energy_reduction_percent": (
                calculate_energy_reduction_percent(
                    baseline_energy,
                    hvac_saving,
                )
            ),
            "cost_saving_inr": round(
                hvac_cost,
                2,
            ),
            "carbon_reduction_kg": round(
                hvac_carbon,
                2,
            ),
            "comfort_impact": hvac_comfort,
            "reason": hvac_reason,
        }
    )

    # ========================================================
    # ACTION 3 - SHIFT FLEXIBLE LOAD
    # ========================================================

    flexible_load_feasible = (
        flexible_load_kwh > 0
        and grid_carbon_intensity >= 400
    )

    if flexible_load_feasible:
        load_saving = (
            flexible_load_kwh * 0.15
        )

        load_reason = (
            "High grid carbon intensity and available flexible "
            "load create an opportunity to shift energy use."
        )

        load_comfort_score = 0.95
        load_comfort = "Very Low"

    else:
        load_saving = 0.0

        load_reason = (
            "Flexible-load shifting is not recommended because "
            "there is insufficient flexible load or grid carbon intensity."
        )

        load_comfort_score = 0.0
        load_comfort = "Not suitable"

    load_carbon = (
        load_saving
        * grid_carbon_intensity
        / 1000
    )

    load_cost = (
        load_saving
        * ELECTRICITY_TARIFF_INR
    )

    load_energy_score = normalize(
        load_saving,
        max(
            flexible_load_kwh
            * FLEXIBLE_LOAD_MAX_SAVING_FRACTION,
            0.01,
        ),
    )

    load_carbon_score = normalize(
        load_carbon,
        max(
            flexible_load_kwh
            * grid_carbon_intensity
            / 1000
            * FLEXIBLE_LOAD_MAX_SAVING_FRACTION,
            0.01,
        ),
    )

    load_cost_score = normalize(
        load_cost,
        max(
            flexible_load_kwh
            * ELECTRICITY_TARIFF_INR
            * FLEXIBLE_LOAD_MAX_SAVING_FRACTION,
            0.01,
        ),
    )

    load_score = (
        calculate_action_score(
            load_energy_score,
            load_carbon_score,
            load_cost_score,
            load_comfort_score,
        )
        if flexible_load_feasible
        else 0.0
    )

    actions.append(
        {
            "action": "Shift flexible load",
            "feasible": flexible_load_feasible,
            "score": load_score,
            "baseline_energy_kwh": round(
                baseline_energy,
                2,
            ),
            "optimized_energy_kwh": round(
                baseline_energy - load_saving,
                2,
            ),
            "energy_saving_kwh": round(
                load_saving,
                2,
            ),
            "energy_reduction_percent": (
                calculate_energy_reduction_percent(
                    baseline_energy,
                    load_saving,
                )
            ),
            "cost_saving_inr": round(
                load_cost,
                2,
            ),
            "carbon_reduction_kg": round(
                load_carbon,
                2,
            ),
            "comfort_impact": load_comfort,
            "reason": load_reason,
        }
    )

    # ========================================================
    # ACTION 4 - NO CHANGE
    # ========================================================

    actions.append(
        {
            "action": "No change",
            "feasible": True,
            "score": 15.0,
            "baseline_energy_kwh": round(
                baseline_energy,
                2,
            ),
            "optimized_energy_kwh": round(
                baseline_energy,
                2,
            ),
            "energy_saving_kwh": 0.0,
            "energy_reduction_percent": 0.0,
            "cost_saving_inr": 0.0,
            "carbon_reduction_kg": 0.0,
            "comfort_impact": "None",
            "reason": (
                "Maintain current operation when the benefits "
                "of other feasible actions are insufficient."
            ),
        }
    )

    # ========================================================
    # RANK ACTIONS
    # ========================================================

    actions.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return actions

def verify_energy_prediction(
    baseline_energy_kwh: float,
    predicted_energy_kwh: float,
    actual_energy_kwh: float,
) -> Dict:
    """
    Compare EcoPilot's predicted energy impact
    with the actual measured result.
    """

    predicted_saving = (
        baseline_energy_kwh
        - predicted_energy_kwh
    )

    actual_saving = (
        baseline_energy_kwh
        - actual_energy_kwh
    )

    actual_reduction_percent = (
        actual_saving
        / baseline_energy_kwh
    ) * 100

    if predicted_saving != 0:
        prediction_error_percent = (
            abs(
                actual_saving
                - predicted_saving
            )
            / abs(predicted_saving)
        ) * 100
    else:
        prediction_error_percent = 0.0

    return {
        "baseline_energy_kwh": round(
            baseline_energy_kwh,
            2,
        ),
        "predicted_energy_kwh": round(
            predicted_energy_kwh,
            2,
        ),
        "actual_energy_kwh": round(
            actual_energy_kwh,
            2,
        ),
        "predicted_saving_kwh": round(
            predicted_saving,
            2,
        ),
        "actual_saving_kwh": round(
            actual_saving,
            2,
        ),
        "actual_reduction_percent": round(
            actual_reduction_percent,
            2,
        ),
        "prediction_error_percent": round(
            prediction_error_percent,
            2,
        ),
    }