# database.py
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from models.base import Base

# Database connection
DB_CONNECTION_STRING = "mssql+pyodbc://sa:sa123#@LAPTOP-43OBHKKQ/RetailOLTP?driver=ODBC+Driver+17+for+SQL+Server"


# Create SQLAlchemy engine
engine = create_engine(DB_CONNECTION_STRING, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Before flush event for updated_at
@event.listens_for(Session, "before_flush")
def update_timestamp(session, flush_context, instances):
    for obj in session.dirty:
        if hasattr(obj, "updated_at"):
            obj.updated_at = datetime.now()