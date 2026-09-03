from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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