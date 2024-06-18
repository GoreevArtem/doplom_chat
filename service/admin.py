from fastapi import Depends, HTTPException, status
from sqlalchemy import and_
from database import models
from database.db import SessionLocal, get_db
from service.get_user import GETUSER
from utils.JWT import JWTBearer


class AdminService(GETUSER):
    def __init__(
            self,
            token=Depends(JWTBearer()),
            session: SessionLocal = Depends(get_db),
    ):
        super().__init__(token=token, session=session)
       
    def get_all_user(self):
        self._get_status()
        return self.session.query(models.User).filter(models.User.id != self.user_id).all()
