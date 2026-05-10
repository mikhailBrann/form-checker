from fastapi import HTTPException, Depends
from authx import AuthX, AuthXConfig, RequestToken
from sqlalchemy import select
import os
from datetime import timedelta

from models.shared.user import User
from schemas.shared.auth.auth_user_sheme import AuthUserScheme

class AuthService:
    def __init__(self, security, session, expire_minutes=60):
        self.security = security
        self.session = session
        self.expire_minutes = expire_minutes

    async def login(self, creeds: AuthUserScheme):
        query = select(User).where(User.email == creeds.login)
        result = await self.session.execute(query)
        user = result.scalars().first() 

        if user and user.verify_password(creeds.password):
            token_uid = str(User.id) + "_dui"
            expires = timedelta(minutes=self.expire_minutes)
            
            return self.security.create_access_token(
                uid=token_uid, 
                expires_delta=expires
            )
        
        return None
    

    async def check_token(self, token: RequestToken = Depends()):
        # верифицируем токен
        try: 
            self.security.verify_token(token=token)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")