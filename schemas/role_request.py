from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RoleRequestCreate(BaseModel):
    pass  # no input needed, just send request

class RoleRequestResponse(BaseModel):
    id: int
    user_id: int
    requested_role: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True