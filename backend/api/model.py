from pydantic import BaseModel
from enum import Enum as pyenum
import uuid

class Unit(str, pyenum):
    TL = "TL"
    EL = "EL"
    G = "g"
    STK = "Stk"
    KOPF = "Kopf"
    PRISE = "Prise"
    ML = "ml"
    ZWEIG = "Zweig"

class UserDB(BaseModel):
    userId: str
    email: str
    firstName: str
    lastName: str

class RecipeSchema(BaseModel):
    title: str
    description: str
    cookingTime: int
    preparationTime: int
    imagePath: str
    userId: str

class RecipeDB(RecipeSchema):
    recipeId: uuid.UUID

class IngredientSchema(BaseModel):
    name: str

class IngredientDB(IngredientSchema):
    ingredientId: uuid.UUID

class RecipeIngredientSchema(BaseModel):
    recipeId: uuid.UUID
    ingredientId: uuid.UUID
    amount: int
    unit: Unit

class RatingSchema(BaseModel):
    userId: str
    recipeId: uuid.UUID
    stars: int

class PreparationStepSchema(BaseModel):
    recipeId: uuid.UUID
    stepNumber: int
    description: str

class PreparationStepDB(PreparationStepSchema):
    stepId: uuid.UUID

class CategorySchema(BaseModel):
    name: str

class CategoryDB(CategorySchema):
    categoryId: uuid.UUID

class RecipeCategorySchema(BaseModel):
    recipeId: uuid.UUID
    categoryId: uuid.UUID

class PublicRecipeSchema(RecipeDB):
    stars: float
    ratingAmount: int
    userName: str

class PublicRecipeIngredientSchema(RecipeIngredientSchema):
    name: str