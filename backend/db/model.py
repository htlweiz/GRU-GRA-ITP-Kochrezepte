from sqlalchemy import Integer, String, ForeignKey, UUID
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
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
    ZWEIG = "Zweig"

class User(Base):
    __tablename__ = "users"

    userId: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    firstName: Mapped[str] = mapped_column(String)
    lastName: Mapped[str] = mapped_column(String)

    recipes: Mapped[List["Recipe"]] = relationship("Recipe", back_populates="user")
    ratings: Mapped[List["Rating"]] = relationship("Rating", back_populates="user")


class Recipe(Base):
    __tablename__ = "recipes"

    recipeId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    cookingTime: Mapped[int] = mapped_column(Integer)
    preparationTime: Mapped[int] = mapped_column(Integer)
    imagePath: Mapped[str] = mapped_column(String)
    userId: Mapped[str] = mapped_column(String, ForeignKey("users.userId"))

    user: Mapped["User"] = relationship("User", back_populates="recipes")
    ingredients: Mapped[List["RecipeIngredient"]] = relationship("RecipeIngredient", back_populates="recipe")
    steps: Mapped[List["PreparationStep"]] = relationship("PreparationStep", back_populates="recipe")
    categories: Mapped[List["RecipeCategory"]] = relationship("RecipeCategory", back_populates="recipe")
    ratings: Mapped[List["Rating"]] = relationship("Rating", back_populates="recipe")


class Ingredient(Base):
    __tablename__ = "ingredients"

    ingredientId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)

    recipes: Mapped[List["RecipeIngredient"]] = relationship("RecipeIngredient", back_populates="ingredient")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipeId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recipes.recipeId"), primary_key=True)
    ingredientId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ingredients.ingredientId"), primary_key=True)
    amount: Mapped[int] = mapped_column(Integer)
    unit: Mapped[Unit] = mapped_column(String)

    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship("Ingredient", back_populates="recipes")


class PreparationStep(Base):
    __tablename__ = "preparation_steps"

    stepId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stepNumber: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    recipeId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recipes.recipeId"))

    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="steps")


class Category(Base):
    __tablename__ = "categories"

    categoryId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)

    recipes: Mapped[List["RecipeCategory"]] = relationship("RecipeCategory", back_populates="category")


class RecipeCategory(Base):
    __tablename__ = "recipes_categories"

    recipeId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recipes.recipeId"), primary_key=True)
    categoryId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.categoryId"), primary_key=True)

    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="categories")
    category: Mapped["Category"] = relationship("Category", back_populates="recipes")


class Rating(Base):
    __tablename__ = "ratings"

    recipeId: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("recipes.recipeId"), primary_key=True)
    userId: Mapped[str] = mapped_column(String, ForeignKey("users.userId"), primary_key=True)
    stars: Mapped[int] = mapped_column(Integer)

    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="ratings")
    user: Mapped["User"] = relationship("User", back_populates="ratings")


Base.metadata.create_all(engine)
