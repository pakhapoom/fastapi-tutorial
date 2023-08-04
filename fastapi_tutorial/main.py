from fastapi import FastAPI
from fastapi_tutorial import models
from fastapi_tutorial.database import engine
from fastapi_tutorial.routers import auth, todos

# uvicorn fastapi_tutorial.main:app --reload
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# add routers
app.include_router(auth.router)
app.include_router(todos.router)