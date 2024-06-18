from fastapi import APIRouter, Depends, status
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
