from database.base import  engine, Base
from models.user import User
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from routers.user_router import router as user_router
from core.limiter import limiter

app = FastAPI()

app.include_router(user_router)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

Base.metadata.create_all(bind=engine)

