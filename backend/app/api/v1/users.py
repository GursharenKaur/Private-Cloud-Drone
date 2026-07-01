from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.user import get_all_users
from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import (
    hash_password,
    get_current_user,
    require_admin,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_users(db)
@router.get("/admin")
def admin_dashboard(
    current_user: User = Depends(require_admin),
):
    return {
        "message": "Welcome, Admin!",
        "user": current_user.username,
    }
@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        role="user",
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
