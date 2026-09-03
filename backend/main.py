from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models import (
    EnergyInput,
    OptimizationResponse,
)
from backend.optimizer import optimize_energy


app = FastAPI(
    title="EcoPilot AI API",
    description=(
        "Adaptive carbon-aware energy optimization "
        "for campuses."
    ),
    version="1.0.0",
)


# Allow the React frontend to communicate with FastAPI
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

    return {
        "building": data.building,
        "recommended_action": best_action["action"],
        "confidence": round(
            min(best_action["score"] + 10, 95),
            2,
        ),
        "actions": actions,
    }