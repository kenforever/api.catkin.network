from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from . import endpoints
import uvicorn

# from .config import config


app = FastAPI()


@app.get("/")
async def root():
    return "Hello World!"


origins = [
    "http://localhost:3002",
    "https://dashboard.catkin.network",
    "http://localhost:3001",
    "http://localhost:3000",
    "http://localhost:3003",
    "http://localhost:3004",
    "http://localhost:3005",
    "http://localhost:3006",
    "http://localhost:3007",
    
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# cloudflare_r2_connection_test()


# def poetry_start():
#     """Launched with `poetry run start` at root level"""
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)


app.include_router(endpoints.router)
