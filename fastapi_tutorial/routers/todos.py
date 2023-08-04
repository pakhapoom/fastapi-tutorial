from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends # dependency injection
from fastapi import Path
from fastapi import HTTPException
from fastapi_tutorial.models import Todos
from fastapi_tutorial.database import SessionLocal
from starlette import status
from pydantic import BaseModel, Field

# uvicorn fastapi_tutorial.main:app --reload
router = APIRouter()

# # to access sqlite3 in termal
# sqlite3 todos.db
# .schema
# .quit # -> exit
# insert into todos (title, description, priority, complete) values ("Go to the store", "Pick up eggs", 5, False);
# insert into todos (title, description, priority, complete) values ("Cut the lawn", "Grass is getting long", 3, False);
# insert into todos (title, description, priority, complete) values ("Feed the dog", "He is getting angry", 5, False);
# select * from todos;
# .mode column # -> change the view to table-like output
# .mode markdown # -> markdown table
# .mode box # -> table with edge
# .mode table

# delete from todos where id = 3; 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: # do once finish
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    # don't have to specify id here because it is automatically added in db
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found.")

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_table(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()