from fastapi import Depends, HTTPException, status
from sqlalchemy import and_

from database import models
from database.db import SessionLocal, get_db, post_singleton
from scheme.scheme import CategoryCreateModel, CategoryUpdateModel
from service.get_user import GETUSER
from utils.JWT import JWTBearer


class AdminService(GETUSER):
    def __init__(
            self,
            token=Depends(JWTBearer()),
            session: SessionLocal = Depends(get_db),
    ):
        super().__init__(token=token, session=session)
    def __get_status(self):
        if not self.session.query(models.User).filter(and_(models.User.role == True, models.User.id == self.user_id)).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Not admin")
        
    def create_category(self, category: CategoryCreateModel):
        self.__get_status()
        post_singleton.create_category(category=category)

    def get_categories(self):
        return post_singleton.get_categories()

    def get_category(self, id: str):
        return post_singleton.get_category(id)

    def update_category(self, id: str, category: CategoryUpdateModel):
        self.__get_status()
        return post_singleton.update_category(id, category)
    
    async def delete_category(self, id: str):
        self.__get_status()
        return post_singleton.delete_category(id)