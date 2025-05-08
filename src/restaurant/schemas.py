from pydantic import BaseModel, PositiveFloat
from typing import Optional

from .models.types import Specialization, Vehicle, OrderType, OrderStatus, created_at, updated_at


# Admin
# Input Forms
class ChefAddDTO(BaseModel):
    name: str
    experience: int
    is_active: bool = True

class CookAddDTO(BaseModel):
    name: str
    experience: int
    specialization: Specialization
    is_active: bool = True
    chef_id: int

class CourierAddDTO(BaseModel):
    name: str
    vehicle: Vehicle
    is_active: bool = True

class DishAddDTO(BaseModel):
    name: str
    price: PositiveFloat
    specialization: Specialization

class OrderAddDTO(BaseModel):
    order_type: OrderType = OrderType.dine_in

# Output data
class ChefDTO(ChefAddDTO):
    id: int

class CookDTO(CookAddDTO):
    id: int

class CourierDTO(CourierAddDTO):
    id: int

class DishDTO(DishAddDTO):
    id: int

class OrderDTO(OrderAddDTO):
    id: int
    order_status: OrderStatus = OrderStatus.preparing
    created_at: created_at
    updated_at: updated_at


# Models Relationships
class ChefCooksRelDTO(ChefDTO):
    cooks: list["CookDTO"]

class CooksChefRelDTO(CookDTO):
    chef: ChefDTO

ChefCooksRelDTO.model_rebuild()
CooksChefRelDTO.model_rebuild()

# Customer
class OrderDishRelAddDTO(BaseModel):
    order_id: int
    dish_id: int
    quantity: Optional[int] = 1

class ReceiptDTO(BaseModel):
    order_id: int
    quantity: int

class OrderReceiptDTO(BaseModel):
    dish: DishDTO
    order: OrderDTO
    total_bill: PositiveFloat
