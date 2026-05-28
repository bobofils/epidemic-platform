from fastapi import APIRouter
from backend.services.simulation_service import simulate

router = APIRouter()


@router.post("/simulate")
def run(data: dict):

    result = simulate(data)

    return result