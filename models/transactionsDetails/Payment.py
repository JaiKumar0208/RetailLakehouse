from sqlalchemy import Column, Integer, DECIMAL, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.base import Base, TimestampMixin

class Payment(Base, TimestampMixin):
    __tablename__ = "payments"
    __table_args__ = {"schema": "dbo"}
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey("dbo.sales_transactions.transaction_id"))
    payment_method = Column(String(50))
    payment_date = Column(DateTime)
    amount = Column(DECIMAL(10,2))

    transaction = relationship("SalesTransaction", back_populates="payments")

