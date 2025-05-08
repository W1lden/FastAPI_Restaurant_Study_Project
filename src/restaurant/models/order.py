from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import text
from ..core.database import Base
from .types import intpk, OrderStatus, created_at, updated_at, OrderType
# from .dish import DishOrm


class OrderOrm(Base):
    __tablename__ = "order"

    id: Mapped[intpk]
    order_type: Mapped[OrderType] = mapped_column(default=OrderType.dine_in)
    order_status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.preparing)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    dishes: Mapped[list["DishOrm"]] = relationship( # type: ignore
        back_populates="orders",
        secondary="order_dish"
    )
