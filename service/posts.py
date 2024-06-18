from fastapi import HTTPException, status
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
import pymongo

from scheme.scheme import CategoryCreateModel, CategoryModel, CategoryUpdateModel, Post, SearchRequest

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PostSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = pymongo.MongoClient(*args, **kwargs)
            cls._instance.db = cls._instance.client.get_database("_BLOG_")
            cls._instance.collection_posts = cls._instance.db.get_collection("_POSTS_")
            cls._instance.collection_category = cls._instance.db.get_collection("_CATEGORY_")
        return cls._instance

    def get_posts(self):
        data = [{**post, '_id': str(post['_id'])} for post in self.collection_posts.find()]
        if not data:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return dict(zip(range(1, len(data) + 1), data))
       
    def get_post(self, post_id: str):
        if not ObjectId.is_valid(post_id):
            raise HTTPException(status_code=400, detail="Invalid ID")
        data=self.collection_posts.find_one({"_id": ObjectId(post_id)})
        if not data:
            raise HTTPException(status.HTTP_409_CONFLICT)
        data['_id'] = str(data['_id'])
        return data

    def add_post(self, post_data):
        result=self.collection_posts.insert_one(post_data.dict())
        if not result.acknowledged:
            raise HTTPException(status.HTTP_409_CONFLICT)
        return {"id": str(result.inserted_id)}

    def delete_post(self, post_id: str):
        result = self.collection_posts.delete_one({"_id": ObjectId(post_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    def delete_all_posts(self):
        result = self.collection_posts.delete_many({})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    def update_post(self, post_id: str, new_data: Post):
        result = self.collection_posts.update_one({"_id": ObjectId(post_id)}, {"$set": new_data.dict()})
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
    def create_category(self, category: CategoryCreateModel):
        if not self.collection_category.find_one({"name": category.name}):
            category = jsonable_encoder(category)
            result = self.collection_category.insert_one(category)
            new_category = self.collection_category.find_one({"_id": result.inserted_id})
            return CategoryModel(**new_category)
        raise HTTPException(status.HTTP_409_CONFLICT, detail="category already exist")
    
    def get_categories(self):
        categories = list(self.collection_category.find())
        return [CategoryModel(**category) for category in categories]

    def get_category(self, id: str):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID")
    
        category = self.collection_category.find_one({"_id": ObjectId(id)})
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        
        return CategoryModel(**category)

    def update_category(self, id: str, category: CategoryUpdateModel):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID")
        if not self.collection_category.find_one({"name": category.name}):
            category = {k: v for k, v in category.dict().items() if v is not None}
            if len(category) >= 1:
                update_result = self.collection_category.update_one({"_id": ObjectId(id)}, {"$set": category})
                
                if update_result.modified_count == 1:
                    updated_category = self.collection_category.find_one({"_id": ObjectId(id)})
                    if updated_category is not None:
                        return CategoryModel(**updated_category)
            
            existing_category = self.collection_category.find_one({"_id": ObjectId(id)})
            if existing_category is not None:
                return CategoryModel(**existing_category)
        
            raise HTTPException(status_code=404, detail="Category not found")
        raise HTTPException(status.HTTP_409_CONFLICT, detail="category already exist")

    def delete_category(self, id: str):
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID")
        
        delete_result = self.collection_category.delete_one({"_id": ObjectId(id)})
        if delete_result.deleted_count == 1:
            return {"detail": "Category deleted"}
        
        raise HTTPException(status_code=404, detail="Category not found")
    
    def search_post(self, search_request: SearchRequest):
        query = search_request.query

        posts_list = [{**post, '_id': str(post['_id'])} for post in self.collection_posts.find()]
        
        if not posts_list:
            raise HTTPException(status_code=404, detail="No posts found")

        # Преобразование данных постов в список текстов
        posts_content = [post["content"] for post in posts_list]

        documents = posts_content + [query]

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents)

        # Вычисление косинусного сходства между запросом и постами
        cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

        # Получение индексов постов, отсортированных по схожести
        similar_indices = cosine_sim.argsort()[::-1]

        # Формирование результата поиска
        similar_posts = [posts_list[i] for i in similar_indices]

        return similar_posts