from fastapi import status, APIRouter, Depends

from scheme import scheme
from service.auth import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    response_model=scheme.UserResponseSchema
)
async def create_user(
        payload: scheme.CreateUserSchema,
        auth_service: AuthService = Depends()
):
    return auth_service.register_new_user(payload)



@router.post(
    '/authenticate',
    status_code=status.HTTP_200_OK,
    response_model=scheme.TokenSchema
)
async def authenticate_user(
        payload: scheme.LoginUserSchema,
        auth_service: AuthService = Depends(),
):
    return auth_service.authenticate_user(payload)