from sqlalchemy import Column, Integer, String, DateTime
from models.base import Base

class WatermarkTable(Base):
    __tablename__ = "watermark_table"
    TableName = Column(String(100), primary_key=True)
    LastLoadDate = Column(DateTime)

