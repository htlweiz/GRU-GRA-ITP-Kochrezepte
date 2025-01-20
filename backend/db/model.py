from sqlalchemy import Integer, String, ForeignKey, UUID
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from db.session import engine
from typing import List
from enum import Enum as pyenum
import uuid

Base = declarative_base()

class Unit(str, pyenum):
    TL = "TL"
    EL = "EL"
    G = "g"
    STK = "Stk"
    KOPF = "Kopf"
    PRISE = "Prise"
    ML = "ml"

class User(Base):
    __tablename__ = "users"

    userId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True)
    firstName: Mapped[str] = mapped_column(String)
    lastName: Mapped[str] = mapped_column(String)

    recipes: Mapped[List["Recipe"]] = mapped_column(List["Recipe"], back_populates="user")
    ratings: Mapped[List["Rating"]] = mapped_column(List["Rating"], back_populates="user")


class Recipe(Base):
    __tablename__ = "recipes"

    recipeId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    cookingTime: Mapped[int] = mapped_column(Integer)
    preparationTime: Mapped[int] = mapped_column(Integer)
    imagePath: Mapped[str] = mapped_column(String)
    userId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.userId"))

    user: Mapped[User] = mapped_column(User, back_populates="recipes")
    ingredients: Mapped[List["RecipeIngredient"]] = mapped_column(List["RecipeIngredient"], back_populates="recipe")
    steps: Mapped[List["PreparationStep"]] = mapped_column(List["PreparationStep"], back_populates="recipe")
    categories: Mapped[List["RecipeCategory"]] = mapped_column(List["RecipeCategory"], back_populates="recipe")
    ratings: Mapped[List["Rating"]] = mapped_column(List["Rating"], back_populates="recipe")


class Ingredient(Base):
    __tablename__ = "ingredients"

    ingredientId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)

    recipes: Mapped[List["RecipeIngredient"]] = mapped_column(List["RecipeIngredient"], back_populates="ingredient")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipeId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recipes.recipeId"), primary_key=True)
    ingredientId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ingredients.ingredientId"), primary_key=True)
    amount: Mapped[int] = mapped_column(Integer)
    unit: Mapped[Unit] = mapped_column(String)

    recipe: Mapped[Recipe] = mapped_column(Recipe, back_populates="ingredients")
    ingredient: Mapped[Ingredient] = mapped_column(Ingredient, back_populates="recipes")


class PreparationStep(Base):
    __tablename__ = "preparation_steps"

    stepId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stepNumber: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    recipeId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recipes.recipeId"))

    recipe: Mapped[Recipe] = mapped_column(Recipe, back_populates="steps")


class Category(Base):
    __tablename__ = "categories"

    categoryId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)

    recipes: Mapped[List["RecipeCategory"]] = mapped_column(List["RecipeCategory"], back_populates="category")


class RecipeCategory(Base):
    __tablename__ = "recipes_categories"

    recipeId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recipes.recipeId"), primary_key=True)
    categoryId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.categoryId"), primary_key=True)

    recipe: Mapped[Recipe] = mapped_column(Recipe, back_populates="categories")
    category: Mapped[Category] = mapped_column(Category, back_populates="recipes")


class Rating(Base):
    __tablename__ = "ratings"

    recipeId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recipes.recipeId"))
    userId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.userId"))
    stars: Mapped[int] = mapped_column(Integer)

    recipe: Mapped[Recipe] = mapped_column(Recipe)
    user: Mapped[User] = mapped_column(User)


Base.metadata.create_all(bind=engine)