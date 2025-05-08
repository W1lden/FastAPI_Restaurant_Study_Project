from sqlalchemy.orm import Mapped, mapped_column
from ..core.database import Base
from .types import intpk, Vehicle


class CourierOrm(Base):
    __tablename__ = "courier"

    id: Mapped[intpk]
    name: Mapped[str]
    vehicle: Mapped[Vehicle]
    is_active: Mapped[bool] = mapped_column(default=True)