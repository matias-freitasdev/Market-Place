from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from database.base import engine, Base
from models.user import User
from models.product import Product
from models.order import Order
from core.limiter import limiter


from routers.user_router import router as user_router
from routers.product_router import router as product_router
from routers.order_router import router as order_router


from exceptions.handlers import register_exception_handlers

app = FastAPI(
    title="Market Place API",
    version="1.0.2",
    swagger_ui_parameters={"theme": "dark"},
)


register_exception_handlers(app)


app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)


app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)

Base.metadata.create_all(bind=engine)