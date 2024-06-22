from datetime import datetime
from fastapi import Depends, HTTPException, status
from sqlalchemy import and_
from database import models
from database.db import SessionLocal, get_db
from scheme import scheme
from service.get_user import GETUSER
from utils import hash_pwd
from utils.JWT import JWTBearer


class AdminService(GETUSER):
    def __init__(
            self,
            token=Depends(JWTBearer()),
            session: SessionLocal = Depends(get_db),
    ):
        super().__init__(token=token, session=session)
    
    def __get_user_by_email(
            self,
            payload: scheme.UserBaseSchema,
    ):
        return self.session.query(models.User).filter(
            models.User.email == payload.email
        ).first()

    def __get_user_by_name(
            self,
            payload: scheme.UserBaseSchema,
    ):
        return self.session.query(models.User).filter(
            models.User.name == payload.name).first()

    def get_all_user(self):
        self._get_status()
        return self.session.query(models.User).filter(models.User.id != self.user_id).all()

    def get_user(self, id: str):
        self._get_status()
        return self.session.query(models.User).get(id)
    
    def update_user(self, id: str, payload: scheme.UserBaseSchema):
        self._get_status()
        user = self.session.query(models.User).get(id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        user.name = payload.name
        user.email = payload.email
        user.password = hash_pwd.hash_password(payload.password)
        user.role = payload.role
                    
        self.session.commit()
        self.session.refresh(user)
             
    
    def delete_user(self, id: str):
        self._get_status()
        if user:= self.session.query(models.User).get(id):
            self.session.delete(user)
            self.session.commit()
            self.session.refresh(user)
             
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    
    def create_user(self, payload: scheme.UserBaseSchema):
        self._get_status()

        if self.__get_user_by_email(payload=payload) or self.__get_user_by_name(payload=payload):
            raise HTTPException(status.HTTP_409_CONFLICT, detail="user already exist")
        new_user = models.User(
            name=payload.name,
            email=payload.email,
            password=payload.password,
            role=payload.role,
            )
            
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)