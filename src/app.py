from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import Request
from fastapi.responses import JSONResponse

from src.app_factory import create_app

# Get the number of applications from the environment variable
app = create_app()

# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )