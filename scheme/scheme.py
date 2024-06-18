from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


class OrmMode(BaseModel):
    class Config:
        from_attributes = True


class UserBaseSchema(OrmMode):
    name: Optional[str]
    email: EmailStr
    password: str


class CreateUserSchema(UserBaseSchema):
    pass


class LoginUserSchema(UserBaseSchema):
    pass


class UpdateUserEmailSchema(OrmMode):
    email: EmailStr


class UpdateUserPasswordSchema(OrmMode):
    password: Optional[str]


class UserResponseSchema(OrmMode):
    name: Optional[str]
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    
    
class Image(BaseModel):
    url: str
    
class Post(BaseModel):
    title: str
    category: List
    content: str
    photo: Union[str, None]


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class CategoryModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class CategoryCreateModel(BaseModel):
    name: str
    description: str

class CategoryUpdateModel(BaseModel):
    name: str = None
    description: str = None


class SearchRequest(BaseModel):
    query: str