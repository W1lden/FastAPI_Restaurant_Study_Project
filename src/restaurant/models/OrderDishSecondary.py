from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from ..core.database import Base
from .types import intpk


class OrderDishOrm(Base):
    __tablename__ = "order_dish"

    order_id: Mapped[intpk] = mapped_column(
        ForeignKey("order.id", ondelete="CASCADE"),
        primary_key=True,
    )
    dish_id: Mapped[intpk] = mapped_column(
        ForeignKey("dish.id", ondelete="CASCADE"),
        primary_key=True,
    )
    quantity: Mapped[Optional[int]] = mapped_column(default=1)
