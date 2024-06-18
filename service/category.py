from fastapi import Depends, HTTPException, status
from sqlalchemy import and_

from database import models
from database.db import SessionLocal, get_db, post_singleton
from scheme.scheme import CategoryCreateModel, CategoryUpdateModel
from service.get_user import GETUSER
from utils.JWT import JWTBearer


class CategoryService(GETUSER):
    def __init__(
            self,
            token=Depends(JWTBearer()),
            session: SessionLocal = Depends(get_db),
    ):
        super().__init__(token=token, session=session)
        
    def create_category(self, category: CategoryCreateModel):
        self._get_status()
        post_singleton.create_category(category=category)

    def get_categories(self):
        data = post_singleton.get_categories()
        return dict(zip(range(1, len(data) + 1), data))

    def get_category(self, id: str):
        return post_singleton.get_category(id)

    def update_category(self, id: str, category: CategoryUpdateModel):
        self._get_status()
        return post_singleton.update_category(id, category)
    
    async def delete_category(self, id: str):
        self._get_status()
        return post_singleton.delete_category(id)