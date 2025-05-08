from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import CheckConstraint

from ..core.database import Base
from ..models.types import intpk

class ChefOrm(Base):
    __tablename__ = "chef"

    id: Mapped[intpk]
    name: Mapped[str]
    experience: Mapped[int] # in years
    is_active: Mapped[bool] = mapped_column(default=True)
    
    cooks: Mapped[list["CookOrm"]] = relationship( # type: ignore
        back_populates="chef"
    )

    __table_args__ = (
        CheckConstraint("experience >= 10", name="check_experience_constraint"),
    )
