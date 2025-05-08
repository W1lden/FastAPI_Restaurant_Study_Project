from enum import Enum
from sqlalchemy import text
from sqlalchemy.orm import mapped_column
from datetime import datetime
from typing import Annotated


# id: Primary key
intpk = Annotated[int, mapped_column(primary_key=True)]

# Cook: Specialization
class Specialization(str, Enum):
    italian = "italian"
    turkish = "turkish"
    japanese = "japanese"
    confectioner = "confectioner"

# Order type
class OrderType(str, Enum):
    dine_in = "dine_in"
    delivery = "delivery"

# Order status
class OrderStatus(str, Enum):
    preparing = "preparing"
    delivering = "delivering"
    delivered = "delivered"
    cancelled = "cancelled"

# DateTime
created_at = Annotated[datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow)]

# Courier: Vehicle
class Vehicle(str, Enum):
    scooter = "scooter"
    bike = "bike"
    car = "car"
