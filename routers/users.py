from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.role_request import RoleRequest
from schemas.user import UserResponse
from schemas.role_request import RoleRequestResponse
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

# Get my profile
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

# Update my profile
@router.patch("/me")
def update_my_profile(
    username: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if username:
        # Check if username taken
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")
        current_user.username = username

    db.commit()
    db.refresh(current_user)
    return {"message": "Profile updated successfully"}

# Request analyst role
@router.post("/request-role", response_model=RoleRequestResponse)
def request_analyst_role(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only viewers can request
    if current_user.role != "viewer":
        raise HTTPException(
            status_code=400,
            detail="Only viewers can request analyst role"
        )

    # Check if already has pending request
    existing_request = db.query(RoleRequest).filter(
        RoleRequest.user_id == current_user.id,
        RoleRequest.status == "pending"
    ).first()

    if existing_request:
        raise HTTPException(
            status_code=400,
            detail="You already have a pending request"
        )

    # Create new request
    new_request = RoleRequest(
        user_id=current_user.id,
        requested_role="analyst"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request