from sqlalchemy import Column, Integer, String, Date, DECIMAL
from sqlalchemy.orm import relationship
from models.base import Base
from models.base import Base, TimestampMixin

class Category(Base, TimestampMixin):
    __tablename__ = "categories"
    __table_args__ = {"schema": "dbo"}
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(100))
    description = Column(String(500))
