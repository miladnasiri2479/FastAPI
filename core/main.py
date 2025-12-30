from fastapi import FastAPI, Depends, Request,HTTPException,status,BackgroundTasks
from starlette.exceptions import HTTPException 
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes
from core.config import settings



tags_metadata = [
    {
        "name": "tasks",
        "description": "Operations related to task management",
        "externalDocs": {
            "description": "More about tasks",
            "url": "https://example.com/docs/tasks",
        },
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")



app = FastAPI(
    title="Todo Application",
    description=(
        "A simple and efficient Todo management API built with FastAPI. "
        "This API allows users to create, retrieve, update, and delete tasks. "
        "It is designed for task tracking and productivity improvement."
    ),
    version="1.0.0",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "Milad Nasiri",
        "email": "Miladnasiri2479@gmail.com",
    },

)
app.include_router(tasks_routes)
