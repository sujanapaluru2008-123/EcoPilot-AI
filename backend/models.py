from pydantic import BaseModel, Field


class EnergyInput(BaseModel):
    building: str = Field(..., min_length=1)
    occupancy_percent: float = Field(..., ge=0, le=100)
    temperature_c: float = Field(..., ge=-20, le=60)
    daylight_level: float = Field(..., ge=0, le=100)
    current_energy_kwh: float = Field(..., gt=0)
    flexible_load_kwh: float = Field(..., ge=0)
    grid_carbon_intensity: float = Field(..., ge=0)


class ActionResult(BaseModel):
    action: str
    feasible: bool
    score: float
    baseline_energy_kwh: float
    optimized_energy_kwh: float
    energy_saving_kwh: float
    energy_reduction_percent: float
    cost_saving_inr: float
    carbon_reduction_kg: float
    comfort_impact: str
    reason: str


class OptimizationResponse(BaseModel):
    building: str
    recommended_action: str
    confidence: float
    actions: list[ActionResult]