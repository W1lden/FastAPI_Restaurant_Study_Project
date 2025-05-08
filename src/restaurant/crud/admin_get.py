from sqlalchemy import select
from ..core.database import async_session_factory
from ..models import (
    ChefOrm,
    CookOrm,
    CourierOrm,
    DishOrm,
    OrderOrm,
)


async def admin_get_all_orders():
    async with async_session_factory() as session:
        query = select(OrderOrm)
        result = await session.execute(query)
        res = result.scalars().all()
        return res
    
async def admin_get_all_workers():
    async with async_session_factory() as session:
        chefs = (await session.execute(select(ChefOrm))).scalars().all()
        cooks = (await session.execute(select(CookOrm))).scalars().all()
        couriers = (await session.execute(select(CourierOrm))).scalars().all()
        return {
            "chefs": chefs,
            "cooks": cooks,
            "couriers": couriers
        }
    
async def admin_get_all_dishes():
    async with async_session_factory() as session:
        query = select(DishOrm)
        result = await session.execute(query)
        res = result.scalars().all()
        print(type(res))
        return res