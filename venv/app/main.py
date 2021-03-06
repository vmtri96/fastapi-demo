from __future__ import annotations
from fastapi import FastAPI, Header, HTTPException, Query, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app import my_session

from .routers.version_1 import login
from .routers.version_1 import user
from .routers.version_1 import role
from .routers.version_1 import product_type
from .routers.version_1 import brand
from .routers.version_1 import status
from .routers.version_1 import product
from .routers.version_1 import upload


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    my_session.initialize()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(login.router,
                   tags=["login"])
app.include_router(user.router,
                   tags=["users"])
app.include_router(role.router,
                   tags=["roles"])
app.include_router(product_type.router,
                   tags=["product type"])
app.include_router(brand.router,
                   tags=["brands"])
app.include_router(status.router,
                   tags=["status"])
app.include_router(product.router,
                   tags=["product"])
app.include_router(upload.router,
                   tags=["upload"])







