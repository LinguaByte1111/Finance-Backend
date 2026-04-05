from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from database import get_db
from models.financial_record import FinancialRecord
from models.user import User
from schemas.financial_record import RecordCreate, RecordUpdate, RecordResponse
from middleware.auth_middleware import get_current_user, require_role

router = APIRouter(prefix="/records", tags=["Financial Records"])

# Create record - Admin only
@router.post("/", response_model=RecordResponse)
def create_record(
    record_data: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    # Validate type
    if record_data.type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Type must be income or expense")

    new_record = FinancialRecord(
        amount=record_data.amount,
        type=record_data.type,
        category=record_data.category,
        date=record_data.date,
        notes=record_data.notes,
        created_by=current_user.id
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

# Get all records - All roles with pagination and filters
@router.get("/")
def get_records(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    type: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(FinancialRecord).filter(FinancialRecord.is_deleted == False)

    # Apply filters
    if type:
        query = query.filter(FinancialRecord.type == type)
    if category:
        query = query.filter(FinancialRecord.category == category)
    if start_date:
        query = query.filter(FinancialRecord.date >= start_date)
    if end_date:
        query = query.filter(FinancialRecord.date <= end_date)

    # Pagination
    total = query.count()
    records = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": records
    }

# Get single record - All roles
@router.get("/{record_id}", response_model=RecordResponse)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = db.query(FinancialRecord).filter(
        FinancialRecord.id == record_id,
        FinancialRecord.is_deleted == False
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return record

# Update record - Admin only
@router.patch("/{record_id}", response_model=RecordResponse)
def update_record(
    record_id: int,
    record_data: RecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    record = db.query(FinancialRecord).filter(
        FinancialRecord.id == record_id,
        FinancialRecord.is_deleted == False
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    if record_data.amount is not None:
        record.amount = record_data.amount
    if record_data.type is not None:
        if record_data.type not in ["income", "expense"]:
            raise HTTPException(status_code=400, detail="Type must be income or expense")
        record.type = record_data.type
    if record_data.category is not None:
        record.category = record_data.category
    if record_data.date is not None:
        record.date = record_data.date
    if record_data.notes is not None:
        record.notes = record_data.notes

    db.commit()
    db.refresh(record)
    return record

# Soft delete record - Admin only
@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    record = db.query(FinancialRecord).filter(
        FinancialRecord.id == record_id,
        FinancialRecord.is_deleted == False
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Soft delete
    record.is_deleted = True
    db.commit()
    return {"message": "Record deleted successfully"}