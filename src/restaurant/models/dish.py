from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, UniqueConstraint
from ..core.database import Base
from .types import intpk, Specialization


class DishOrm(Base):
    __tablename__ = "dish"

    id: Mapped[intpk]
    name: Mapped[str]
    price: Mapped[float]
    specialization: Mapped[Specialization]

    orders: Mapped[list["OrderOrm"]] = relationship( # type: ignore
        back_populates="dishes",
        secondary="order_dish"
    )

    __table_args__ = (
        CheckConstraint("price > 0", name="check_price_positive"),
        # UniqueConstraint("name", name="check_unique_dish_name")
    )
