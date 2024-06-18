from typing import Dict
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from redis.commands.json.path import Path
from scheme.scheme import Post, SearchRequest
from database.db import post_singleton, redis_startup
from utils.JWT import JWTBearer

router = APIRouter(
    prefix='/posts',
    tags=['posts'],
)

@router.post("/create_post", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK, response_model=Dict[str, str])
async def create_post(post: Post):
    return post_singleton.add_post(post)

@router.get("/get_all_posts",
            status_code=status.HTTP_200_OK
            )
async def get_posts():
    key = "get_all_posts"
    if redis_startup.json().get(key) is None:
        data = post_singleton.get_posts()
        redis_startup.json().set(key, Path.root_path(), jsonable_encoder(data))
        redis_startup.expire(key, 30)
    return redis_startup.json().get(key)

@router.get("/get_post/{post_id}",
            status_code=status.HTTP_200_OK,
            )
async def get_posts(post_id: str):
    return post_singleton.get_post(post_id)

@router.patch("/update_post/{post_id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
async def update_post(post_id: str, post: Post):
    return post_singleton.update_post(post_id, post)

@router.delete("/delete_post/{post_id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
async def  delete_post(post_id: str):
    return post_singleton.delete_post(post_id)

@router.delete("/delete_all_posts", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_post():
    return post_singleton.delete_all_posts()

@router.post("/search")
async def search_posts(search_request: SearchRequest):
    return post_singleton.search_post(search_request)