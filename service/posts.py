from fastapi import HTTPException, status
from bson import ObjectId
import pymongo

from scheme.scheme import Post

class PostSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = pymongo.MongoClient(*args, **kwargs)
            cls._instance.db = cls._instance.client.get_database("_BLOG_")
            cls._instance.collection = cls._instance.db.get_collection("_POSTS_")
        return cls._instance

    def get_posts(self):
        data = [{**post, '_id': str(post['_id'])} for post in self.collection.find()]
        if not data:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return dict(zip(range(1, len(data) + 1), data))
       
    def get_post(self, post_id: str):
        data=self.collection.find_one({"_id": ObjectId(post_id)})
        if not data:
            raise HTTPException(status.HTTP_409_CONFLICT)
        data['_id'] = str(data['_id'])
        return data

    def add_post(self, post_data):
        result=self.collection.insert_one(post_data.dict())
        if not result.acknowledged:
            raise HTTPException(status.HTTP_409_CONFLICT)
        return {"id": str(result.inserted_id)}

    def delete_post(self, post_id: str):
        result = self.collection.delete_one({"_id": ObjectId(post_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    def delete_all_posts(self):
        result = self.collection.delete_many({})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    def update_post(self, post_id: str, new_data: Post):
        result = self.collection.update_one({"_id": ObjectId(post_id)}, {"$set": new_data.dict()})
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")