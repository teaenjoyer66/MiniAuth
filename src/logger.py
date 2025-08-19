import logging
import pandas as pd 
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path

Base = declarative_base()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
DATA_DIR = ROOT_DIR / 'data'
CSV_FILEPATH = DATA_DIR / "logs.csv"
DB_FILEPATH = DATA_DIR / "logs.db"

class ServiceLog(Base):
    __tablename__ = "service_logs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String, nullable=False)
    details = Column(String, nullable=False)

class Logger:
    def __init__(self, db_path: Path = DB_FILEPATH, csv_path: Path = CSV_FILEPATH):
        self.db_path = Path(db_path)
        self.csv_path = Path(csv_path)

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)

        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def log_event(self, event_type: str, details: str) -> None:
        try:
            with self.SessionLocal() as session:
                entry = ServiceLog(event_type=event_type, details=details)
                session.add(entry)
                session.commit()
        except Exception as e:
            logging.error(f"Failed to log event: {e}")
    
    def export_to_csv(self) -> None:        
        try:
            with self.SessionLocal() as session:
                logs = session.query(ServiceLog).all()
                df = pd.DataFrame([{
                    "id": log.id,
                    "timestamp": log.timestamp,
                    "event_type": log.event_type,
                    "details": log.details
                } for log in logs])
                df.to_csv(self.csv_path, index=False, encoding="utf-8")
        except Exception as e:
            logging.error(f"Failed to export logs to CSV: {e}")