from sqlalchemy.orm import Session
from datetime import datetime
from models.etl import ETLRunLog


class ETLRunLogService:

    @staticmethod
    def start_run(db: Session, pipeline_name: str) -> ETLRunLog:
        run = ETLRunLog(
            PipelineName=pipeline_name,
            Status="RUNNING",
            StartTime=datetime.utcnow()
        )
        db.add(run)
        db.commit()
        db.refresh(run)
        return run

    @staticmethod
    def complete_run(db: Session, run_id: int, records: int = None):
        run = db.query(ETLRunLog).filter_by(RunID=run_id).first()
        run.Status = "SUCCESS"
        run.EndTime = datetime.utcnow()
        run.RecordsProcessed = records
        db.commit()

    @staticmethod
    def fail_run(db: Session, run_id: int, error_message: str):
        run = db.query(ETLRunLog).filter_by(RunID=run_id).first()
        run.Status = "FAILED"
        run.EndTime = datetime.utcnow()
        run.ErrorMessage = error_message
        db.commit()


