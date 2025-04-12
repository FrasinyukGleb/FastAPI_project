from typing import Annotated, List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.exceptions import HTTPException

from src.auth.auth import authenticate_user, create_access_token, reg_user, user_dependency
from src.db.db import db_dependency
from src.schemas.user import UserLoginSchema

auth_router = APIRouter(prefix="/auth", tags=['auth'])


@auth_router.post("/login")
async def login_for_access_token(db: db_dependency,
                                login_data: UserLoginSchema):
   user = await authenticate_user(login_data, db)
   if not user:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Incorrect username or password",
           headers={"WWW-Authenticate": "Bearer"},
       )
   access_token = create_access_token(
       data={"sub": user.email, "role": user.role.name.value}
   )
   return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/token")
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
               db: db_dependency):
   user = await authenticate_user(
       UserLoginSchema(email=form_data.username, password=form_data.password),
       db=db)

   if not user:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                           detail="Could not validate user.")
   access_token = create_access_token(
       data={"sub": user.email, "role": user.role.name.value}
   )
   return {'access_token': access_token, 'token_type': 'bearer'}

@auth_router.get("/current_user")
async def get_current_user(user: user_dependency):
    return {"user": user}

def has_role(required_role: List[str]):
    def role_checker(current_user: user_dependency):
        if current_user["role"] not in required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker