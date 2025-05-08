from typing import Literal
from fastapi import APIRouter, HTTPException

from ..crud.database_setup import admin_create_tables, admin_post_data
from ..crud.admin_get import admin_get_all_orders, admin_get_all_workers, admin_get_all_dishes
from ..crud.admin_cud import admin_add_entity, admin_update_entity, admin_delete_data, admin_prepare_orders
from ..models import (
    ChefOrm,
    CookOrm,
    CourierOrm,
    DishOrm,
)
from ..schemas import (
    ChefAddDTO,
    CookAddDTO,
    CourierAddDTO,
    DishAddDTO
)

router = APIRouter(
    prefix="/admin",
    tags=["AdminPanel"]
)

models_map = {
    "chef": ChefOrm,
    "cook": CookOrm,
    "courier": CourierOrm,
    "dish": DishOrm,
    }

DTOs_map = {
    "chef": ChefAddDTO,
    "cook": CookAddDTO,
    "courier": CourierAddDTO,
    "dish": DishAddDTO,
}

# GET
@router.get("/get_all_orders")
async def get_all_orders():
    result = await admin_get_all_orders()
    return result

@router.get("/get_all_workers")
async def get_all_workers():
    result = await admin_get_all_workers()
    return result

@router.get("/get_menu")
async def get_menu():
    result = await admin_get_all_dishes()
    return result

# ---------------------------------------------------------------------------------------

# POST
@router.post("/post_database", summary="Use 'tables' or 'data'") # POST TABLES
async def post_database(target: Literal["tables", "data"]):
    if target == "tables":
        try:
            await admin_create_tables()
            return {"message": "All tables have been created."}
        except Exception as e:
            print(f"Error creating tables: {e}")
            raise HTTPException(status_code=500, detail="Failed to create tables.")
    elif target == "data":
        try:
            await admin_post_data()
            return {"message": "All data has been setup."}
        except Exception as e:
            print(f"Error creating tables: {e}")
            raise HTTPException(status_code=500, detail="Failed to setup data.")

# POST CHEF
@router.post("/post_chef", summary="Add Chef", response_model=ChefAddDTO)
async def post_chef(chef: ChefAddDTO):
    new_chef = await admin_add_entity(chef, ChefOrm)
    return ChefAddDTO.model_validate(new_chef, from_attributes=True)

# POST COOK
@router.post(
    "/post_cook", 
    summary="Add Cook with speciality: italian, turkish, japanese or confectioner", 
    response_model=CookAddDTO
)
async def post_cook(cook: CookAddDTO):
    new_cook = await admin_add_entity(cook, CookOrm)
    return CookAddDTO.model_validate(new_cook, from_attributes=True)

# POST COURIER
@router.post(
    "/post_courier", 
    summary="Add Courier with vehicle type: scooter, bike or car", 
    response_model=CourierAddDTO
)
async def post_courier(courier: CourierAddDTO):
    new_courier = await admin_add_entity(courier, CourierOrm)
    return CourierAddDTO.model_validate(new_courier, from_attributes=True)

# POST DISH
@router.post(
    "/post_dish", 
    summary="Add Dish with cuisine: italian, turkish, japanese or confectioner", 
    response_model=DishAddDTO
)
async def post_dish(dish: DishAddDTO):
    new_dish = await admin_add_entity(dish, DishOrm)
    return DishAddDTO.model_validate(new_dish, from_attributes=True)


# ---------------------------------------------------------------------------------------

# PUT CHEF
@router.put(
    "/put_chef", 
    summary="Update chef by it's id", 
    response_model=ChefAddDTO
)
async def put_chef(id: int, chef: ChefAddDTO):
    chef_updated = await admin_update_entity(chef, ChefOrm, id)
    return ChefAddDTO.model_validate(chef_updated, from_attributes=True)

# PUT COOK
@router.put(
    "/put_cook", 
    summary="Update cook by it's id", 
    response_model=CookAddDTO
)
async def put_cook(id: int, cook: CookAddDTO):
    cook_updated = await admin_update_entity(cook, CookOrm, id)
    return CookAddDTO.model_validate(cook_updated, from_attributes=True)

# PUT COURIER
@router.put(
    "/put_courier", 
    summary="Update courier by it's id", 
    response_model=CourierAddDTO
)
async def put_courier(id: int, courier: CourierAddDTO):
    courier_updated = await admin_update_entity(courier, CourierOrm, id)
    return CourierAddDTO.model_validate(courier_updated, from_attributes=True)

# PUT DISH
@router.put(
    "/put_dish", 
    summary="Update dish by it's id", 
    response_model=DishAddDTO
)
async def put_chef(id: int, dish: DishAddDTO):
    dish_updated = await admin_update_entity(dish, DishOrm, id)
    return DishAddDTO.model_validate(dish_updated, from_attributes=True)

# PUT ORDER
@router.put("/put_order", summary="Prepare customer's orders")
async def put_order():
    result = await admin_prepare_orders()
    return result

# ---------------------------------------------------------------------------------------

# DELETE
@router.delete("/delete_data", summary="Delete entity by it's id")
async def delete_data(
    target: Literal["chef", "cook", "courier", "dish"],
    id: int    
):
    try:
        model = models_map.get(target)
        if model:
            deleted_data = await admin_delete_data(id, model)
            return {"message": f"Delete {model.__name__} with id: {id}. {deleted_data}"}
        else:
            raise HTTPException(status_code=404, detail="No model found.")
    except Exception as e:
        print(f"Error deleting tables: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete data.")
