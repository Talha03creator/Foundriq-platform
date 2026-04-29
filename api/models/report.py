import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from api.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    validation_score = Column(Float, nullable=True)
    competition_score = Column(Float, nullable=True)
    risk_level = Column(String(50), nullable=True)
    swot = Column(JSON, nullable=True)
    revenue_forecast = Column(JSON, nullable=True)
    strategy_steps = Column(JSON, nullable=True)
    break_even = Column(JSON, nullable=True)
    full_report = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

