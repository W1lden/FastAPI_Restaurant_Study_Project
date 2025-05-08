from typing import Literal
from fastapi import APIRouter, HTTPException

from ..crud.cusomer_cru import customer_get_all_dishes, customer_make_order, customer_get_order_status
from ..models import (
    ChefOrm,
    CookOrm,
    CourierOrm,
    DishOrm,
    OrderOrm,
)
from ..schemas import (
    ChefAddDTO,
    CookAddDTO,
    CourierAddDTO,
    DishAddDTO,
    OrderReceiptDTO
)


router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)

# GET
@router.get("/get_menu", response_model=list[DishAddDTO])
async def get_menu():
    menu = await customer_get_all_dishes()
    return [
        DishAddDTO(name=name, specialization=specialization, price=price)
        for name, specialization, price in menu
    ]

@router.get("/get_order_status")
async def get_order_status(order_id: int):
    order_status = await customer_get_order_status(order_id)
    return order_status

# ----------------------------------------------------------------------------------------

# POST
@router.post("/make_order", summary="See dish name on menu.")
async def make_order(dish_name: str, order_type: Literal["dine_in", "delivery"], quantity: int = 1):
    receipt = await customer_make_order(dish_name, order_type, quantity)
    return receipt


@router.post("/make_delivery")
async def make_delivery():
    pass

# ----------------------------------------------------------------------------------------

# PUT
@router.put("/edit_order")
async def edit_order():
    pass
