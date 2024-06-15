from typing import Dict
from fastapi import APIRouter, status

from scheme.scheme import Post
from database.db import post_singleton

router = APIRouter(
    prefix='/posts',
    tags=['posts'],
)

# Создание нового рецепта
@router.post("/create_post", status_code=status.HTTP_200_OK, response_model=Dict[str, str])
async def create_post(post: Post):
    return post_singleton.add_post(post)

# Получение рецептов
@router.get("/get_all_posts",
            status_code=status.HTTP_200_OK
            )
async def get_posts():
    return post_singleton.get_posts()

@router.get("/get_post/{post_id}",
            status_code=status.HTTP_200_OK,
            )
async def get_posts(post_id: str):
    return post_singleton.get_post(post_id)


# Обновление рецепта
@router.patch("/update_post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(post_id: str, post: Post):
    return post_singleton.update_post(post_id, post)

# Удаление рецепта
@router.delete("/delete_post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def  delete_post(post_id: str):
    return post_singleton.delete_post(post_id)

# Удаление всех постов
@router.delete("/delete_all_posts", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_post():
    return post_singleton.delete_all_posts()