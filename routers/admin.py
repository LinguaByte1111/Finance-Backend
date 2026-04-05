from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.role_request import RoleRequest
from middleware.auth_middleware import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])

# Get all users
@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    users = db.query(User).all()
    return users

# Activate or deactivate user
@router.patch("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = is_active
    db.commit()
    return {"message": f"User {'activated' if is_active else 'deactivated'} successfully"}

# Get all pending role requests
@router.get("/role-requests")
def get_role_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    requests = db.query(RoleRequest).filter(RoleRequest.status == "pending").all()
    return requests

# Approve role request
@router.patch("/role-requests/{request_id}/approve")
def approve_role_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    role_request = db.query(RoleRequest).filter(RoleRequest.id == request_id).first()
    if not role_request:
        raise HTTPException(status_code=404, detail="Request not found")

    if role_request.status != "pending":
        raise HTTPException(status_code=400, detail="Request already processed")

    # Update request status
    role_request.status = "approved"
    role_request.reviewed_by = current_user.id

    # Update user role
    user = db.query(User).filter(User.id == role_request.user_id).first()
    user.role = "analyst"

    db.commit()
    return {"message": "Role request approved successfully"}

# Reject role request
@router.patch("/role-requests/{request_id}/reject")
def reject_role_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    role_request = db.query(RoleRequest).filter(RoleRequest.id == request_id).first()
    if not role_request:
        raise HTTPException(status_code=404, detail="Request not found")

    if role_request.status != "pending":
        raise HTTPException(status_code=400, detail="Request already processed")

    role_request.status = "rejected"
    role_request.reviewed_by = current_user.id

    db.commit()
    return {"message": "Role request rejected"}

# Revoke analyst role
@router.patch("/users/{user_id}/revoke")
def revoke_analyst_role(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role != "analyst":
        raise HTTPException(status_code=400, detail="User is not an analyst")

    user.role = "viewer"
    db.commit()
    return {"message": "Analyst role revoked successfully"}