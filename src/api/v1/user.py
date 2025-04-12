from fastapi import APIRouter, HTTPException
from starlette import status

from src.auth.auth import reg_user
from src.db.db import db_dependency
from src.schemas.user import UserRegisterSchema

user_router = APIRouter(prefix="/user", tags=['user'])

@user_router.post("/register")
async def register_user(user_data: UserRegisterSchema, db: db_dependency):
    try:
        return await reg_user(user_data=user_data, db=db)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Аn error has occurred: {ex}")


# @user_router.post("/login")
# async def login_for_access_token(db: db_dependency,
#                                  login_data: UserLoginSchema):
#     user = await authenticate_user(login_data, db)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(
#         data={"sub": {"email": user.email, "role": user.role.name.value}}
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

