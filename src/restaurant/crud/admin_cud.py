import asyncio
import time
import random
from sqlalchemy import select, update
from fastapi import HTTPException

from ..core.database import async_session_factory, Base
from ..models.order import OrderOrm
from ..models.types import OrderStatus


# POST
async def admin_add_entity(dto, model):
    async with async_session_factory() as session:
        entity = model(**dto.dict())
        session.add(entity)        

        await session.commit()
        await session.refresh(entity)

        return entity


# PUT
async def admin_update_entity(dto, model, id):
    async with async_session_factory() as session:
        entity = await session.get(model, id)
        if entity is None:
            return HTTPException(status_code=404, detail="Entity not found.")
        
        for key, value in dto.dict().items():
            setattr(entity, key, value)

        await session.commit()
        await session.refresh(entity)

        return entity
    

# Async queue
async def cook_order(order: OrderOrm) -> tuple[int, bool]:
    """
    Возвращает кортеж: (ID заказа, True — если удалось приготовить, False — если нет)
    """
    start = time.perf_counter()
    print(f"👨‍🍳 Повар готовит заказ №{order.id}...")
    await asyncio.sleep(random.uniform(1, 3))
    cook_time = time.perf_counter() - start
    print(f"✅ Заказ №{order.id} готов за {cook_time:.2f} сек")

    try:
        async with async_session_factory() as session:
            stmt = (
                update(OrderOrm)
                .where(OrderOrm.id == order.id)
                .values(order_status=OrderStatus.delivered)
            )
            await session.execute(stmt)
            await session.commit()
        print(f"🟢 Статус заказа №{order.id} обновлён на delivered")
        return order.id, True
    except Exception as e:
        print(f"❌ Не удалось обновить заказ №{order.id}: {e}")
        return order.id, False

async def admin_prepare_orders():
    async with async_session_factory() as session:
        query = select(OrderOrm).where(OrderOrm.order_status == OrderStatus.preparing)
        results = await session.execute(query)
        orders_to_prepare = results.scalars().all()

    if not orders_to_prepare:
        return {
            "message": "Нет заказов к приготовлению.",
            "prepared": [],
            "failed": []
        }

    tasks = [asyncio.create_task(cook_order(order)) for order in orders_to_prepare]
    results = await asyncio.gather(*tasks)

    prepared = [order_id for order_id, success in results if success]
    failed = [order_id for order_id, success in results if not success]

    return {
        "message": f"Обработано заказов: {len(results)}. Успешно: {len(prepared)}, с ошибками: {len(failed)}.",
        "prepared": prepared,
        "failed": failed
    }

# DELETE
async def admin_delete_data(id: int, model: Base):
    async with async_session_factory() as session:
        query = select(model, id)
        result = await session.execute(query)
        instance = result.scalars().first()

        if not instance:
            return None
        
        await session.delete(instance)
        await session.commit()

        return instance
