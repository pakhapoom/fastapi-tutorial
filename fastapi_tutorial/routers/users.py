# import: standard
from typing import Annotated

# import: fastapi
from fastapi import APIRouter  # dependency injection
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from starlette import status

# import: internal
from fastapi_tutorial.database import SessionLocal
from fastapi_tutorial.models import Users
from fastapi_tutorial.routers.auth import get_current_user

# import: external
from passlib.context import CryptContext
from pydantic import BaseModel
from pydantic import Field
from sqlalchemy.orm import Session

# uvicorn fastapi_tutorial.main:app --reload
router = APIRouter(
    prefix="/user",
    tags=["user"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:  # do once finish
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(
    user: user_dependency,
    db: db_dependency,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentiation failed.")
    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    user_verification: UserVerification,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not bcrypt_context.verify(
        user_verification.password,
        user_model.hashed_password,
    ):
        raise HTTPException(status_code=401, detail="Error on password change.")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
