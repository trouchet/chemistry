from fastapi import APIRouter
from prometheus_client import Counter, generate_latest

router = APIRouter()

requests_counter = Counter("requests_total", "Total number of requests")

@router.get("/metrics")
async def metrics():
    requests_counter.inc()
    return generate_latest()