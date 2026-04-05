from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date
from datetime import datetime
from database import Base

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String)        # income or expense
    category = Column(String)
    date = Column(Date)
    notes = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False)  # soft delete
    created_by = Column(Integer)  # user id
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)