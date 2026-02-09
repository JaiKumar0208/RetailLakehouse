from sqlalchemy import Column, Integer, DECIMAL, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.base import Base, TimestampMixin

class SalesTransaction(Base, TimestampMixin):
    __tablename__ = "sales_transactions"
    __table_args__ = {"schema": "dbo"}
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey("dbo.stores.store_id"))
    product_id = Column(Integer, ForeignKey("dbo.products.product_id"))
    customer_id = Column(Integer, ForeignKey("dbo.customers.customer_id"))
    quantity = Column(Integer)
    sale_amount = Column(DECIMAL(10,2))
    sale_date = Column(DateTime)
    last_modified = Column(DateTime)

    store = relationship("Store", back_populates="sales")
    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    payments = relationship("Payment", back_populates="transaction")
    returns = relationship("SalesReturn", back_populates="transaction")

