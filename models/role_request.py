from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class RoleRequest(Base):
    __tablename__ = "role_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    requested_role = Column(String, default="analyst")
    status = Column(String, default="pending")  # pending, approved, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_by = Column(Integer, nullable=True)  # admin user id