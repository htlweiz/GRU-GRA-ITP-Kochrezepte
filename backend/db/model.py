from sqlalchemy import Integer, String, ForeignKey, DateTime, Table, Column, Boolean, UUID
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from db.session import engine
from datetime import datetime
from typing import List
from enum import Enum as pyenum
import uuid

Base = declarative_base()




Base.metadata.create_all(bind=engine)