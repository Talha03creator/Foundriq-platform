import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from api.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    business_idea = Column(Text, nullable=False)
    target_market = Column(String(500), nullable=False)
    budget = Column(Float, nullable=True)
    pricing_model = Column(String(255), nullable=True)
    competitors = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

