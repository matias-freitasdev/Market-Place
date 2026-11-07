from sqlalchemy import String, Integer, Boolean, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base
from datetime import datetime

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] =  mapped_column(Integer, primary_key=True)
    buyer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    saller_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    total: Mapped[int] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[int] = mapped_column(String(30), default="pending")