from sqlalchemy import Column, Integer, String, Date, DECIMAL
from sqlalchemy.orm import relationship
from models.base import Base

class Calendar(Base):
    __tablename__ = "calendar"
    __table_args__ = {"schema": "dbo"}
    date = Column(Date, primary_key=True)
    year = Column(Integer)
    quarter = Column(Integer)
    month = Column(Integer)
    month_name = Column(String(20))
    day = Column(Integer)
    week_day = Column(String(20))

