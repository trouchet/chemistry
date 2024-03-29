from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler

from routes import recommendation, security

# Initialize the app
app = FastAPI()

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

app.include_router(security.router, prefix="/api/", tags=["users"])
app.include_router(recommendation.router, prefix="/api/recommendation", tags=["items"])

# Handle validation errors
@app.exception_handler(HTTPException)
async def validation_exception_handler(request, exc):
    return {"detail": exc.detail}

# Handle unexpected errors
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return {"detail": "Internal server error"}
