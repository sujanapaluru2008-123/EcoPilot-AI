from backend.optimizer import optimize_energy


def test_optimizer_returns_actions():

    results = optimize_energy(
        occupancy_percent=35,
        temperature_c=29,
        daylight_level=85,
        current_energy_kwh=120,
        flexible_load_kwh=20,
        grid_carbon_intensity=550,
    )

    assert len(results) >= 4


def test_actions_are_sorted_by_score():

    results = optimize_energy(
        occupancy_percent=35,
        temperature_c=29,
        daylight_level=85,
        current_energy_kwh=120,
        flexible_load_kwh=20,
        grid_carbon_intensity=550,
    )

    scores = [result["score"] for result in results]

    assert scores == sorted(scores, reverse=True)


def test_energy_savings_are_non_negative():

    results = optimize_energy(
        occupancy_percent=35,
        temperature_c=29,
        daylight_level=85,
        current_energy_kwh=120,
        flexible_load_kwh=20,
        grid_carbon_intensity=550,
    )

    for result in results:

        assert result["energy_saving_kwh"] >= 0


def test_no_change_has_zero_savings():

    results = optimize_energy(
        occupancy_percent=35,
        temperature_c=29,
        daylight_level=85,
        current_energy_kwh=120,
        flexible_load_kwh=20,
        grid_carbon_intensity=550,
    )

    no_change = next(
        result
        for result in results
        if result["action"] == "No change"
    )

    assert no_change["energy_saving_kwh"] == 0
    assert no_change["cost_saving_inr"] == 0
    assert no_change["carbon_reduction_kg"] == 0