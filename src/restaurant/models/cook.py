from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core.database import Base
from ..models.types import intpk, Specialization


class CookOrm(Base):
    __tablename__ = "cook"

    id: Mapped[intpk]
    name: Mapped[str]
    experience: Mapped[int] # in years
    specialization: Mapped[Specialization]
    is_active: Mapped[bool] = mapped_column(default=True)
    chef_id: Mapped[int] = mapped_column(ForeignKey("chef.id", ondelete="CASCADE"))

    chef: Mapped["ChefOrm"] = relationship( # type: ignore
        back_populates="cooks"
    )
