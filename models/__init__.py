"""
Top-level models package.

This file makes all ORM models easily importable from:
    from models import Store, Product, SalesTransaction, Payment
"""

# Base declarative class
from .base import Base

# -----------------------------
# Master Tables
# -----------------------------
from .master import (
    Store,
    Product,
    Customer,
    Supplier,
    Employee,
    Category,
)


# -----------------------------
# Transaction Tables
# -----------------------------
from .transactionsDetails import (
    InventoryMovement,
    Payment,
    PurchaseOrder,
    SalesReturn,
    SalesTransaction,
)



# -----------------------------
# ETL / Staging Tables
# -----------------------------
from .etl import (
    ETLRunLog,
    WatermarkTable,
    ETLStepRunLog,
)

# What gets imported when using: from models import *
__all__ = [
    "Base",

    # Master
    "Store",
    "Product",
    "Customer",
    "Supplier",
    "Employee",
    "Category",

    # Transactions
    "SalesTransaction",
    "InventoryMovement",
    "Payment",
    "PurchaseOrder",
    "Return",

    # ETL
    "ETLRunLog",
    "WatermarkTable",
]