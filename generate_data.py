import random
from datetime import datetime, timedelta

import pandas as pd


# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------

BUILDINGS = [
    "Engineering Block",
    "Library",
    "Admin Block",
    "Innovation Centre",
    "Hostel Block",
]

START_DATE = datetime(2026, 8, 1)

DAYS = 14

HOURS = range(8, 20)


# ------------------------------------------------------------
# DATA GENERATION
# ------------------------------------------------------------

rows = []

for day in range(DAYS):

    current_date = START_DATE + timedelta(days=day)

    for hour in HOURS:

        timestamp = current_date.replace(
            hour=hour,
            minute=0,
            second=0,
            microsecond=0,
        )

        for building in BUILDINGS:

            # ------------------------------------------------
            # Occupancy
            # ------------------------------------------------

            if building == "Hostel Block":
                occupancy = random.randint(35, 95)

            else:
                occupancy = random.randint(20, 90)

            # ------------------------------------------------
            # Temperature
            # ------------------------------------------------

            base_temperature = 27 + (
                3 * ((hour - 8) / 11)
            )

            temperature = round(
                base_temperature
                + random.uniform(-1.5, 1.5),
                1,
            )

            # ------------------------------------------------
            # Daylight
            # ------------------------------------------------

            daylight = max(
                0,
                100 - abs(13 - hour) * 10
                + random.randint(-8, 8),
            )

            daylight = min(daylight, 100)

            # ------------------------------------------------
            # Energy Consumption
            # ------------------------------------------------

            base_energy = {
                "Engineering Block": 120,
                "Library": 90,
                "Admin Block": 70,
                "Innovation Centre": 100,
                "Hostel Block": 110,
            }[building]

            occupancy_factor = occupancy / 100

            energy = (
                base_energy
                * (0.65 + 0.35 * occupancy_factor)
                + random.uniform(-8, 8)
            )

            energy = round(
                max(energy, 20),
                2,
            )

            # ------------------------------------------------
            # Flexible Load
            # ------------------------------------------------

            flexible_load = round(
                max(
                    energy * random.uniform(0.08, 0.20),
                    0,
                ),
                2,
            )

            # ------------------------------------------------
            # Grid Carbon Intensity
            # ------------------------------------------------

            carbon_intensity = random.randint(
                400,
                600,
            )

            # ------------------------------------------------
            # Store Row
            # ------------------------------------------------

            rows.append(
                {
                    "timestamp": timestamp,
                    "building": building,
                    "occupancy_percent": occupancy,
                    "temperature_c": temperature,
                    "daylight_level": daylight,
                    "current_energy_kwh": energy,
                    "flexible_load_kwh": flexible_load,
                    "grid_carbon_intensity": carbon_intensity,
                }
            )


# ------------------------------------------------------------
# CREATE DATAFRAME
# ------------------------------------------------------------

df = pd.DataFrame(rows)


# ------------------------------------------------------------
# SAVE CSV
# ------------------------------------------------------------

output_path = "data/campus_energy.csv"

df.to_csv(
    output_path,
    index=False,
)


print("Dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Buildings: {df['building'].nunique()}")
print(f"Saved to: {output_path}")