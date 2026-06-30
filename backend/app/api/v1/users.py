from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.user import get_all_users
from app.database.database import get_db
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return get_all_users(db)
