from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from routers.hashing import Hash
from routers.schemas import User
import routers.models as models


def creat(request: User, db: Session):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_id(
    id: int,
    db: Session,
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )
    return user
