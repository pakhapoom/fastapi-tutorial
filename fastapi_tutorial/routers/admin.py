# import: standard
from typing import Annotated

# import: fastapi
from fastapi import APIRouter
from fastapi import Depends  # dependency injection
from fastapi import HTTPException
from fastapi import Path
from starlette import status

# import: internal
from fastapi_tutorial.database import SessionLocal
from fastapi_tutorial.models import Todos
from fastapi_tutorial.routers.auth import get_current_user

# import: external
from pydantic import BaseModel
from pydantic import Field
from sqlalchemy.orm import Session

# uvicorn fastapi_tutorial.main:app --reload
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:  # do once finish
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(
    user: user_dependency,
    db: db_dependency,
):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentiation failed.")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentiation failed.")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
