from fastapi import APIRouter, Depends, status, HTTPException
from routers.database import get_db
from sqlalchemy.orm import Session
from routers.hashing import Hash
import routers.models as models
from .token import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from routers.schemas import Token

Router = APIRouter(tags=["Authentication"])


@Router.post("/loging", response_model=Token)
def loging(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials",
        )
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incorrect password",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
