from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.session import metadata, engine

from api import users


metadata.create_all(engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
