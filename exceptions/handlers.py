from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )