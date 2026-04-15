from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from services.user_service import UserService
from database import SESSION_DEPENDENCY
from services.user_service import UserService
from schemas.user.user_add_sheme import UserAddSheme
from schemas.user.user_pub_sheme import UserPubSheme

router = APIRouter()

@router.get(
    "/find-by-id/{user_id}", 
    summary="Поиск пользователя по ID", 
    response_model=UserPubSheme
)
async def find_by_id(user_id: int, session: SESSION_DEPENDENCY):
    service = UserService(session)
    user = await service.get_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    return user

@router.get(
    "/find-by-email", 
    summary="Поиск пользователя по email", 
    response_model=UserPubSheme
)
async def find_by_email(session: SESSION_DEPENDENCY, user_email: str = Query(...)):
    service = UserService(session)
    user = await service.get_by_email(user_email)

    if not user:
        raise HTTPException(status_code=404, detail=f"User with email {user_email} not found")

    return user

@router.post(
    "/", 
    summary="Создать пользователя", 
    response_model=UserPubSheme
)
async def add_user(data: UserAddSheme, session: SESSION_DEPENDENCY):
    service = UserService(session)
    input_email = data.email
    user = await service.get_by_email(input_email)

    if user:
        raise HTTPException(status_code=404, detail=f"User with email {input_email} is exist")

    new_user = await service.create(data.dict())

    return new_user
