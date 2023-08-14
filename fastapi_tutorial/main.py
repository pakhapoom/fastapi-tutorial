# import: fastapi
from fastapi import FastAPI

# import: internal
from fastapi_tutorial import models
from fastapi_tutorial.database import engine
from fastapi_tutorial.routers import admin
from fastapi_tutorial.routers import auth
from fastapi_tutorial.routers import todos
from fastapi_tutorial.routers import users

# uvicorn fastapi_tutorial.main:app --reload
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# add routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
