from fastapi import APIRouter
import toml

router = APIRouter()

@router.get('/ping')
async def pong():
    return {"message": "pong"}

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/info")
async def info():
    with open("pyproject.toml", "r") as f:
        config = toml.load(f)
    
    return {
        "name": config["tool"]["poetry"]["name"],
        "version": config["tool"]["poetry"]["version"],
        "description": config["tool"]["poetry"]["description"]
    }