from sqlalchemy import select
from fastapi import HTTPException
from ..core.database import async_session_factory
from ..models import (
    ChefOrm,
    CookOrm,
    CourierOrm,
    DishOrm,
    OrderOrm,
    OrderDishOrm
)
from ..schemas import OrderDTO, DishDTO, OrderReceiptDTO


async def customer_get_all_dishes():
    async with async_session_factory() as session:
        query = select(DishOrm.name, DishOrm.specialization, DishOrm.price)
        result = await session.execute(query)
        res = result.all()

        return res

async def customer_make_order(dish_name: str, order_type: str, quantity: int):
    async with async_session_factory() as session:
        # 1. Find the dish by it's name in Dish table
        query = select(DishOrm).where(DishOrm.name == dish_name).limit(1)
        result = await session.execute(query)

        dish = result.scalar_one()
        order = OrderOrm(order_type=order_type)
        session.add(order)
        await session.flush()

        # 2. Add order by dish id to OrderDishSecondary table
        total_bill = quantity * dish.price
        order_dish = OrderDishOrm(order_id=order.id, dish_id=dish.id, quantity=quantity)
        
        session.add(order_dish)

        dish_dto = DishDTO.model_validate(dish, from_attributes=True)
        order_dto = OrderDTO.model_validate(order, from_attributes=True)
        order_receipt = OrderReceiptDTO(
            dish=dish_dto,
            order=order_dto,
            total_bill=total_bill
        )
        await session.commit()
        return order_receipt

async def customer_get_order_status(order_id: int):
    async with async_session_factory() as session:
        order = await session.get(OrderOrm, order_id)
        return order

