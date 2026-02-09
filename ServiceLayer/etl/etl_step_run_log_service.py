from sqlalchemy.orm import Session
from datetime import datetime
from models.etl.etl_step_run_log import ETLStepRunLog


class ETLStepRunLogService:

    @staticmethod
    def start_step(db: Session, run_id: int, step_name: str) -> ETLStepRunLog:
        step = ETLStepRunLog(
            RunID=run_id,
            StepName=step_name,
            Status="RUNNING",
            StartTime=datetime.utcnow()
        )
        db.add(step)
        db.commit()
        db.refresh(step)
        return step

    @staticmethod
    def complete_step(db: Session, step_id: int, records: int = None):
        step = db.query(ETLStepRunLog).filter_by(StepRunID=step_id).first()
        step.Status = "SUCCESS"
        step.EndTime = datetime.utcnow()
        step.RecordsProcessed = records
        db.commit()

    @staticmethod
    def fail_step(db: Session, step_id: int, error_message: str):
        step = db.query(ETLStepRunLog).filter_by(StepRunID=step_id).first()
        step.Status = "FAILED"
        step.EndTime = datetime.utcnow()
        step.ErrorMessage = error_message[:500]
        db.commit()
