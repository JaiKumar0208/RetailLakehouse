from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.base import Base, TimestampMixin

class Employee(Base, TimestampMixin):
    __tablename__ = "employees"
    __table_args__ = {"schema": "dbo"}
    employee_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_name = Column(String(100))
    store_id = Column(Integer, ForeignKey("dbo.stores.store_id"))
    salary = Column(Integer)
    dob = Column(Date)

    store = relationship("Store", back_populates="employees")
