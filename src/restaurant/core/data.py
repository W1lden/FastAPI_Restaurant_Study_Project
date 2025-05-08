import sys
import os
import random
import pandas as pd
from collections import defaultdict
from datetime import datetime
from faker import Faker
from faker_food import FoodProvider

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ..models.types import Specialization, Vehicle, OrderType, OrderStatus


fake = Faker()
fake.add_provider(FoodProvider)

# Data generators

# Chefs
chefs = [
    {"name": fake.name(), "experience": random.randint(10, 40), "is_active": True}
    ] + [
    {"name": fake.name(), "experience": random.randint(10, 40), "is_active": False}
    for _ in range(2, 7)
]

# Cooks
cooks = [
    {"name": fake.name(), "experience": random.randint(1, 9), "specialization": random.choice(list(Specialization)),
     "chef_id": random.randint(1, 6), "is_active": random.choices([True, False], weights=[0.3, 0.7])[0]}
    for _ in range(1, 31)
]

# Couriers
couriers = [
    {"name": fake.name(), "vehicle": random.choice(list(Vehicle)), "is_active": random.choices([True, False], weights=[0.3, 0.7])[0]}
    for _ in range(1, 5)
]

dishes_id = [id for id in range(1, 21)]
orders_id = [id for id in range(1, 101)]
orders_dishes_id = [id for id in range(1, 101)]

# Dishes
dishes = [
    {"name": "Doner with chicken", "price": 3.99, "specialization": "turkish"}
    ] + [
    {"name": fake.dish(), "price": random.randint(10, 100), "specialization": random.choice(list(Specialization))}
    for _ in dishes_id
]

# Orders
orders = [
    {"order_type": random.choice(list(OrderType)), "order_status": OrderStatus.delivered,
     "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
    for _ in orders_id
]

# Yet to optimize ↓↓↓

# Generate 100 order_dish rows
orders_data = defaultdict(list)
for i in range(1, 101):
    dish_num = random.choices([1, 2, 3, 4], weights=[70, 25, 4, 1])[0] # A customer picked a random amount of dishes 
    for _ in range(1, dish_num + 1): # Pick random dishes
        orders_data[i + 1].append(random.choice(dishes_id))

# Converti int(id): list(dishes) to int: str, example - 1: [1, 2, 3] → 1: 1, 1: 2, 1: 3
my_order_dish = []
for order_id, order_dish in orders_data.items():
    for dish_id in order_dish:
        my_order_dish.append({"order_id": order_id, "dish_id": dish_id})

# Remove duplicates
df = pd.DataFrame(my_order_dish)
df.drop_duplicates(subset=["order_id", "dish_id"], keep="first", inplace=True)
my_order_dish_set = df.to_dict("records")

# Order-Dish (связующая таблица)
order_dish = [
    {"order_id": row["order_id"], "dish_id": row["dish_id"]}
    for row in my_order_dish_set
]
