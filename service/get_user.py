from fastapi import Depends, HTTPException, status

from database import models
from database.db import SessionLocal, get_db
from utils.JWT import JWTBearer


class GETUSER:
    def __init__(
            self,
            token=Depends(JWTBearer()),
            session: SessionLocal = Depends(get_db),
    ):
        self.token = token
        self.user_id = JWTBearer.decodeJWT(token).get("user_id")
        self.session = session

    def _get_user_by_id(
            self
    ):
        user = self.session.query(models.User).get(self.user_id)
        if user is not None:
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Not authenticated',
                headers={"WWW-Authenticate": "Bearer"},
            )
