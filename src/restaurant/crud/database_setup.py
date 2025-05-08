from ..core.data import chefs, cooks, couriers, dishes, orders, order_dish
from ..core.database import Base, async_engine, async_session_factory
from ..models import *


model_data_map = {
    ChefOrm: chefs,
    CookOrm: cooks,
    CourierOrm: couriers,
    DishOrm: dishes,
    OrderOrm: orders,
}

async def admin_create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def admin_post_data():
    async with async_session_factory() as session:
        # 1. Add first pack of data, exluding the secondary table order_dish
        for model, data in model_data_map.items():
            for values in data:
                try:
                    session.add(model(**values))
                except Exception as e:
                    print(f"\nError in {model.__name__} with {values}: {e}\n")
        await session.commit()

        # 2. Add next pack of data, including the secondary table order_dish
        for values in order_dish:
            try:
                session.add(OrderDishOrm(**values))
                await session.flush()
                await session.commit()
            except Exception as e:
                print(f"\nError in {OrderDishOrm.__name__} with {values}: {e}\n")

