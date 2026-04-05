from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Optional
from datetime import date, datetime, timedelta
from database import get_db
from models.financial_record import FinancialRecord
from models.user import User
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# Helper function to get date range
def get_date_range(period: str):
    today = date.today()
    if period == "1day":
        return today, today
    elif period == "1week":
        return today - timedelta(weeks=1), today
    elif period == "1month":
        return today - timedelta(days=30), today
    elif period == "3months":
        return today - timedelta(days=90), today
    elif period == "6months":
        return today - timedelta(days=180), today
    elif period == "1year":
        return today - timedelta(days=365), today
    else:  # max - all time
        return None, None

# Total income, expenses, net balance
@router.get("/summary")
def get_summary(
    period: str = Query(default="max", enum=["1day", "1week", "1month", "3months", "6months", "1year", "max"]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start_date, end_date = get_date_range(period)

    base_query = db.query(FinancialRecord).filter(
        FinancialRecord.is_deleted == False
    )

    if start_date and end_date:
        base_query = base_query.filter(
            FinancialRecord.date >= start_date,
            FinancialRecord.date <= end_date
        )

    total_income = base_query.filter(
        FinancialRecord.type == "income"
    ).with_entities(func.sum(FinancialRecord.amount)).scalar() or 0

    total_expenses = base_query.filter(
        FinancialRecord.type == "expense"
    ).with_entities(func.sum(FinancialRecord.amount)).scalar() or 0

    return {
        "period": period,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": total_income - total_expenses
    }

# Category wise totals
@router.get("/categories")
def get_category_totals(
    period: str = Query(default="max", enum=["1day", "1week", "1month", "3months", "6months", "1year", "max"]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start_date, end_date = get_date_range(period)

    query = db.query(
        FinancialRecord.category,
        FinancialRecord.type,
        func.sum(FinancialRecord.amount).label("total")
    ).filter(
        FinancialRecord.is_deleted == False
    )

    if start_date and end_date:
        query = query.filter(
            FinancialRecord.date >= start_date,
            FinancialRecord.date <= end_date
        )

    results = query.group_by(
        FinancialRecord.category,
        FinancialRecord.type
    ).all()

    return {
        "period": period,
        "data": [
            {"category": r.category, "type": r.type, "total": r.total}
            for r in results
        ]
    }

# Monthly trends
@router.get("/trends")
def get_monthly_trends(
    year: Optional[int] = Query(default=None),
    period: str = Query(default="max", enum=["1day", "1week", "1month", "3months", "6months", "1year", "max"]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start_date, end_date = get_date_range(period)

    query = db.query(
        extract("month", FinancialRecord.date).label("month"),
        extract("year", FinancialRecord.date).label("year"),
        FinancialRecord.type,
        func.sum(FinancialRecord.amount).label("total")
    ).filter(
        FinancialRecord.is_deleted == False
    )

    if start_date and end_date:
        query = query.filter(
            FinancialRecord.date >= start_date,
            FinancialRecord.date <= end_date
        )

    if year:
        query = query.filter(extract("year", FinancialRecord.date) == year)

    results = query.group_by(
        "month", "year", FinancialRecord.type
    ).order_by("year", "month").all()

    return {
        "period": period,
        "data": [
            {
                "year": int(r.year),
                "month": int(r.month),
                "type": r.type,
                "total": r.total
            }
            for r in results
        ]
    }

# Recent activity
@router.get("/recent")
def get_recent_activity(
    limit: int = Query(default=5, ge=1, le=20),
    period: str = Query(default="max", enum=["1day", "1week", "1month", "3months", "6months", "1year", "max"]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start_date, end_date = get_date_range(period)

    query = db.query(FinancialRecord).filter(
        FinancialRecord.is_deleted == False
    )

    if start_date and end_date:
        query = query.filter(
            FinancialRecord.date >= start_date,
            FinancialRecord.date <= end_date
        )

    records = query.order_by(
        FinancialRecord.created_at.desc()
    ).limit(limit).all()

    return {
        "period": period,
        "data": records
    }