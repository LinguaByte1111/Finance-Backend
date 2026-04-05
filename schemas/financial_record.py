from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

class RecordCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: date
    notes: Optional[str] = None

    @field_validator("amount")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

    @field_validator("type")
    def type_must_be_valid(cls, v):
        if v not in ["income", "expense"]:
            raise ValueError("Type must be income or expense")
        return v

    @field_validator("category")
    def category_must_be_valid(cls, v):
        if len(v) < 2:
            raise ValueError("Category must be at least 2 characters")
        return v

class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None

    @field_validator("amount")
    def amount_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

    @field_validator("type")
    def type_must_be_valid(cls, v):
        if v is not None and v not in ["income", "expense"]:
            raise ValueError("Type must be income or expense")
        return v

class RecordResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: date
    notes: Optional[str]
    is_deleted: bool
    created_by: int

    class Config:
        from_attributes = True