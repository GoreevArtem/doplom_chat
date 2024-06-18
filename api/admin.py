from fastapi import APIRouter, Depends, status

from scheme.scheme import CategoryCreateModel, CategoryUpdateModel
from service.admin import AdminService
from utils.JWT import JWTBearer


router = APIRouter(
    prefix='/category',
    tags=['category'],
)

@router.post("/categories/", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreateModel, admin_service: AdminService = Depends()):
    return admin_service.create_category(category=category)

@router.get("/categories/", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
async def get_categories(admin_service: AdminService = Depends()):
    return admin_service.get_categories()

@router.get("/categories/{id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
async def get_category(id: str, admin_service: AdminService = Depends()):
    return admin_service.get_category(id)

@router.put("/categories/{id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
async def update_category(id: str, category: CategoryUpdateModel, admin_service: AdminService = Depends()):
    return admin_service.update_category(id, category)

@router.delete("/categories/{id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id: str, admin_service: AdminService = Depends()):
    return admin_service.delete_category(id)