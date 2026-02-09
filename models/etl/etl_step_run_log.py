from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from models.base import Base


class ETLStepRunLog(Base):
    __tablename__ = "etl_step_run_log"

    StepRunID = Column(Integer, primary_key=True, autoincrement=True)
    RunID = Column(Integer, ForeignKey("etl_run_log.RunID"))
    StepName = Column(String(150))
    StartTime = Column(DateTime)
    EndTime = Column(DateTime)
    Status = Column(String(50))
    RecordsProcessed = Column(Integer)
    ErrorMessage = Column(String(500))
