import time

from fastapi import status, Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from database import models
from database.db import get_db
from scheme import scheme
from setting.settings import settings
from utils import hash_pwd


class AuthService:

    def __init__(
            self,
            session: Session = Depends(get_db),

    ):
        self.session = session

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

    @staticmethod
    def _not_user(user):
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Incorrect your data')

    @staticmethod
    def _verify_password(payload, user):
        if not hash_pwd.verify_password(payload.password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Incorrect your data')

    @staticmethod
    def _create_token(user):
        payload = {
            "user_id": str(user.id),
            "expires": time.time() + settings.ACCESS_TOKEN_EXPIRES_IN * 60
        }
        access_token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return access_token

    @staticmethod
    def _delete_token(user, access_token):
        del access_token[str(user.id)]

    def register_new_user(
            self,
            payload: scheme.CreateUserSchema
    ) -> scheme.UserResponseSchema:
        if self.__get_user_by_email(payload) or self.__get_user_by_name(payload):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Account already exist'
            )
        payload.password = hash_pwd.hash_password(payload.password)

        new_user = models.User(**payload.dict())

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def authenticate_user(
            self,
            payload: scheme.LoginUserSchema,
    ) -> scheme.TokenSchema:
        user = self.__get_user_by_email(payload)
        self._not_user(user)
        self._verify_password(payload, user)
        access_token = self._create_token(user=user)
        return scheme.TokenSchema(access_token=access_token)
