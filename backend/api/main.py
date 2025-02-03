from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from db.session import metadata, engine

from api import users, recipes, categories, ingredients, preparation_steps, ratings

metadata.create_all(engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, tags=["users"])
app.include_router(recipes.router, tags=["recipes"])
app.include_router(categories.router, tags=["categories"])
app.include_router(ingredients.router, tags=["ingredients"])
app.include_router(preparation_steps.router, tags=["preparation_steps"])
app.include_router(ratings.router, tags=["ratings"])
