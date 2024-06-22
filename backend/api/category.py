from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from redis.commands.json.path import Path
from database.db import redis_startup
from scheme.scheme import CategoryCreateModel, CategoryUpdateModel
from service.category import CategoryService
from utils.JWT import JWTBearer

router = APIRouter(
    prefix='/category',
    tags=['category'],
)

@router.post("/categories/", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreateModel, category_service: CategoryService = Depends()):
    return category_service.create_category(category=category)

@router.get("/categories/", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
async def get_categories(category_service: CategoryService = Depends()):
    key = "get_categories"
    if redis_startup.json().get(key) is None:
        data = category_service.get_categories()
        redis_startup.json().set(key, Path.root_path(), jsonable_encoder(data))
        redis_startup.expire(key, 15)
    return redis_startup.json().get(key)

@router.get("/categories/{id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
async def get_category(id: str, category_service: CategoryService = Depends()):
    return category_service.get_category(id)

@router.put("/categories/{id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
async def update_category(id: str, category: CategoryUpdateModel, category_service: CategoryService = Depends()):
    return category_service.update_category(id, category)

@router.delete("/categories/{id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id: str, category_service: CategoryService = Depends()):
    return category_service.delete_category(id)