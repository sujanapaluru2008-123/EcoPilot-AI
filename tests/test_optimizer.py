
from backend.optimizer import optimize_energy


def get_test_results():
    return optimize_energy(
        occupancy_percent=35,
        temperature_c=29,
        daylight_level=85,
        current_energy_kwh=120,
        flexible_load_kwh=20,
        grid_carbon_intensity=550,
    )


def test_optimizer_returns_actions():
    results = get_test_results()

    assert len(results) == 4


def test_actions_are_sorted_by_score():
    results = get_test_results()

    scores = [result["score"] for result in results]

    assert scores == sorted(scores, reverse=True)


def test_energy_savings_are_non_negative():
    results = get_test_results()

    for result in results:
        assert result["energy_saving_kwh"] >= 0


def test_no_change_has_zero_savings():
    results = get_test_results()

    no_change = next(
        result
        for result in results
        if result["action"] == "No change"
    )

    assert no_change["energy_saving_kwh"] == 0
    assert no_change["cost_saving_inr"] == 0
    assert no_change["carbon_reduction_kg"] == 0
    assert no_change["energy_reduction_percent"] == 0


# ============================================================
# NEW TESTS
# ============================================================

def test_lighting_action_is_feasible_under_good_conditions():
    results = get_test_results()

    lighting = next(
        result
        for result in results
        if result["action"] == "Reduce lighting load"
    )

    assert lighting["feasible"] is True
    assert lighting["energy_saving_kwh"] > 0


def test_hvac_action_is_feasible_when_temperature_is_high():
    results = get_test_results()

    hvac = next(
        result
        for result in results
        if result["action"] == "Adjust HVAC setpoint by 1°C"
    )

    assert hvac["feasible"] is True
    assert hvac["energy_saving_kwh"] > 0


def test_flexible_load_is_not_feasible_when_no_flexible_load_exists():
    results = optimize_energy(
        occupancy_percent=35,
        temperature_c=29,
        daylight_level=85,
        current_energy_kwh=120,
        flexible_load_kwh=0,
        grid_carbon_intensity=550,
    )

    flexible_load = next(
        result
        for result in results
        if result["action"] == "Shift flexible load"
    )

    assert flexible_load["feasible"] is False
    assert flexible_load["energy_saving_kwh"] == 0


def test_carbon_reduction_is_calculated_correctly():
    results = get_test_results()

    lighting = next(
        result
        for result in results
        if result["action"] == "Reduce lighting load"
    )

    expected_carbon = (
        lighting["energy_saving_kwh"]
        * 550
        / 1000
    )

    assert lighting["carbon_reduction_kg"] == round(
        expected_carbon,
        2,
    )


def test_cost_saving_is_calculated_correctly():
    results = get_test_results()

    lighting = next(
        result
        for result in results
        if result["action"] == "Reduce lighting load"
    )

    expected_cost = (
        lighting["energy_saving_kwh"]
        * 8
    )

    assert lighting["cost_saving_inr"] == round(
        expected_cost,
        2,
    )


def test_optimized_energy_is_never_above_baseline():
    results = get_test_results()

    for result in results:
        assert (
            result["optimized_energy_kwh"]
            <= result["baseline_energy_kwh"]
        )


def test_energy_reduction_percentage_is_valid():
    results = get_test_results()

    for result in results:
        assert 0 <= result["energy_reduction_percent"] <= 100