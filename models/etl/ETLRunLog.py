from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from models.base import Base


class ETLRunLog(Base):
    __tablename__ = "etl_run_log"

    RunID = Column(Integer, primary_key=True, autoincrement=True)

    PipelineName = Column(String(100), nullable=False)

    Status = Column(String(50), nullable=False)
    # RUNNING / SUCCESS / FAILED

    StartTime = Column(DateTime(timezone=True), server_default=func.now())
    EndTime = Column(DateTime(timezone=True), nullable=True)

    RecordsProcessed = Column(Integer, nullable=True)

    ErrorMessage = Column(Text, nullable=True)  # stores exception details

    def __repr__(self):
        return (
            f"<ETLRunLog(RunID={self.RunID}, Pipeline='{self.PipelineName}', "
            f"Status='{self.Status}', Start='{self.StartTime}', End='{self.EndTime}')>"
        )
