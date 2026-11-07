from sqlalchemy import String, Integer, Boolean, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,unique=True,index=True)

    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )