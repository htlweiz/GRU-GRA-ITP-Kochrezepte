from db.session import session
from db.model import User, Recipe, Ingredient, PreparationStep, RecipeIngredient, Category, RecipeCategory, Rating, Unit
import uuid
from api.model import UserDB

async def create_user(user: UserDB):
    db_user = User(
        userId=user.userId,
        email=user.email,
        firstName=user.firstName,
        lastName=user.lastName,
    )
    session.add(db_user)
    session.commit()
    return db_user


async def get_user(user_id: uuid.UUID):
    return session.query(User).filter(User.userId == user_id).first()

async def get_users():
    return session.query(User).all()

async def update_user(user_id: uuid.UUID, user: User):
    db_user = session.query(User).filter(User.userId == user_id).first()
    if db_user is None:
        return None
    db_user.email = user.email
    db_user.firstName = user.firstName
    db_user.lastName = user.lastName
    session.commit()
    return db_user


async def delete_user(user_id: uuid.UUID):
    db_user = session.query(User).filter(User.userId == user_id).first()
    if db_user is None:
        return None
    session.delete(db_user)
    session.commit()
    return db_user