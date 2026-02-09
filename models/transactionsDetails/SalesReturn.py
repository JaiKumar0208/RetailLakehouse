from sqlalchemy import Column, Integer, DECIMAL, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.base import Base, TimestampMixin

class SalesReturn(Base, TimestampMixin):
    __tablename__ = "sales_returns"
    return_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey("dbo.sales_transactions.transaction_id"))
    product_id = Column(Integer, ForeignKey("dbo.products.product_id"))
    customer_id = Column(Integer, ForeignKey("dbo.customers.customer_id"))
    return_date = Column(DateTime)
    refund_amount = Column(DECIMAL(10,2))
    reason = Column(String(200))

    transaction = relationship("SalesTransaction", back_populates="returns")
    product = relationship("Product", back_populates="returns")
    customer = relationship("Customer", back_populates="returns")

