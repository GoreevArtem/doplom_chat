from fastapi import APIRouter, Depends, status
from scheme import scheme
from service.admin import AdminService


router = APIRouter(
    prefix='/admin',
    tags=['admin'],
)


@router.get(
    '/get_all_user',
    status_code=status.HTTP_200_OK
)
async def get_all_user(
        admin_service: AdminService = Depends()
):
    return admin_service.get_all_user()

@router.get("/get_user", status_code=status.HTTP_200_OK)
async def get_user(id: str, admin_service: AdminService = Depends()):
    return admin_service.get_user(id)

@router.delete("/delete_user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str, admin_service: AdminService = Depends()):
    return admin_service.delete_user(id)

@router.patch("/update_user", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(id: str, payload: scheme.UserBaseSchema, admin_service: AdminService = Depends()):
    return admin_service.update_user(id, payload=payload)

@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(payload: scheme.UserBaseSchema, admin_service: AdminService = Depends()):
    return admin_service.create_user(payload=payload)