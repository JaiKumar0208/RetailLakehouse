from sqlalchemy import Column, Integer, String, Date, DECIMAL
from sqlalchemy.orm import relationship
from models.base import Base
from models.base import Base, TimestampMixin

class Customer(Base, TimestampMixin):
    __tablename__ = "customers"
    __table_args__ = {"schema": "dbo"}
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    gender = Column(String(10))
    city = Column(String(100))
    signup_date = Column(Date)

    sales = relationship("SalesTransaction", back_populates="customer")
    returns = relationship("SalesReturn", back_populates="customer")
