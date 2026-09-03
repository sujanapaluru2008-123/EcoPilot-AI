from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.data_service import (
    get_buildings,
    get_latest_reading,
    get_building_history,
)

from backend.models import (
    EnergyInput,
    OptimizationResponse,
    VerificationInput,
    VerificationResponse,
)

from backend.optimizer import (
    optimize_energy,
    calculate_confidence,
    verify_energy_prediction,
)


app = FastAPI(
    title="EcoPilot AI API",
    description=(
        "Adaptive carbon-aware energy optimization "
        "for campuses."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "EcoPilot AI API",
    }


@app.post(
    "/analyze",
    response_model=OptimizationResponse,
)
def analyze_energy(data: EnergyInput):

    actions = optimize_energy(
        occupancy_percent=data.occupancy_percent,
        temperature_c=data.temperature_c,
        daylight_level=data.daylight_level,
        current_energy_kwh=data.current_energy_kwh,
        flexible_load_kwh=data.flexible_load_kwh,
        grid_carbon_intensity=data.grid_carbon_intensity,
    )

    best_action = actions[0]

    confidence = calculate_confidence(actions)

    return {
        "building": data.building,
        "recommended_action": best_action["action"],
        "confidence": confidence,
        "actions": actions,
    }

@app.post(
    "/verify",
    response_model=VerificationResponse,
)
def verify_energy(data: VerificationInput):

    result = verify_energy_prediction(
        baseline_energy_kwh=data.baseline_energy_kwh,
        predicted_energy_kwh=data.predicted_energy_kwh,
        actual_energy_kwh=data.actual_energy_kwh,
    )

    return result

@app.get("/buildings")
def list_buildings():

    return {
        "buildings": get_buildings()
    }


@app.get("/readings/{building}")
def latest_building_reading(building: str):

    try:
        return get_latest_reading(building)

    except ValueError as error:
        return {
            "error": str(error)
        }

@app.get("/dashboard/{building}")
def dashboard_data(building: str):

    try:
        reading = get_latest_reading(building)

    except ValueError as error:
        return {
            "error": str(error)
        }

    actions = optimize_energy(
        occupancy_percent=reading["occupancy_percent"],
        temperature_c=reading["temperature_c"],
        daylight_level=reading["daylight_level"],
        current_energy_kwh=reading["current_energy_kwh"],
        flexible_load_kwh=reading["flexible_load_kwh"],
        grid_carbon_intensity=reading[
            "grid_carbon_intensity"
        ],
    )

    best_action = actions[0]

    confidence = calculate_confidence(actions)

    return {
        "building": building,
        "timestamp": reading["timestamp"],

        "current_conditions": {
            "occupancy_percent": reading[
                "occupancy_percent"
            ],
            "temperature_c": reading[
                "temperature_c"
            ],
            "daylight_level": reading[
                "daylight_level"
            ],
            "current_energy_kwh": reading[
                "current_energy_kwh"
            ],
            "flexible_load_kwh": reading[
                "flexible_load_kwh"
            ],
            "grid_carbon_intensity": reading[
                "grid_carbon_intensity"
            ],
        },

        "recommendation": {
            "action": best_action["action"],
            "confidence": confidence,
            "energy_saving_kwh": best_action[
                "energy_saving_kwh"
            ],
            "energy_reduction_percent": best_action[
                "energy_reduction_percent"
            ],
            "cost_saving_inr": best_action[
                "cost_saving_inr"
            ],
            "carbon_reduction_kg": best_action[
                "carbon_reduction_kg"
            ],
            "comfort_impact": best_action[
                "comfort_impact"
            ],
            "reason": best_action["reason"],
        },

        "actions": actions,
    }

@app.get("/history/{building}")
def building_history(
    building: str,
    limit: int = 24,
):

    try:
        history = get_building_history(
            building,
            limit,
        )

        return {
            "building": building,
            "history": history,
        }

    except ValueError as error:
        return {
            "error": str(error)
        }