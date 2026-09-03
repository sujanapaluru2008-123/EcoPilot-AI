from pathlib import Path

import pandas as pd


# Find the project root:
# EcoPilot-AI/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "campus_energy.csv"


def load_energy_data() -> pd.DataFrame:
    """
    Load the synthetic campus energy dataset.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    return df


def get_buildings() -> list[str]:
    """
    Return the list of available buildings.
    """

    df = load_energy_data()

    return sorted(
        df["building"].unique().tolist()
    )


def get_latest_reading(building: str) -> dict:
    """
    Return the latest available reading
    for a selected building.
    """

    df = load_energy_data()

    building_data = df[
        df["building"] == building
    ]

    if building_data.empty:
        raise ValueError(
            f"Building not found: {building}"
        )

    latest = building_data.sort_values(
        "timestamp"
    ).iloc[-1]

    return {
        "timestamp": latest["timestamp"].isoformat(),
        "building": latest["building"],
        "occupancy_percent": float(
            latest["occupancy_percent"]
        ),
        "temperature_c": float(
            latest["temperature_c"]
        ),
        "daylight_level": float(
            latest["daylight_level"]
        ),
        "current_energy_kwh": float(
            latest["current_energy_kwh"]
        ),
        "flexible_load_kwh": float(
            latest["flexible_load_kwh"]
        ),
        "grid_carbon_intensity": float(
            latest["grid_carbon_intensity"]
        ),
    }

def get_building_history(
    building: str,
    limit: int = 24,
) -> list[dict]:
    """
    Return recent historical readings
    for a selected building.
    """

    df = load_energy_data()

    building_data = df[
        df["building"] == building
    ].sort_values("timestamp")

    if building_data.empty:
        raise ValueError(
            f"Building not found: {building}"
        )

    recent_data = building_data.tail(limit)

    history = []

    for _, row in recent_data.iterrows():
        history.append(
            {
                "timestamp": row["timestamp"].isoformat(),
                "energy_kwh": float(
                    row["current_energy_kwh"]
                ),
                "occupancy_percent": float(
                    row["occupancy_percent"]
                ),
                "carbon_intensity": float(
                    row["grid_carbon_intensity"]
                ),
            }
        )

    return history