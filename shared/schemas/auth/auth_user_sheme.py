from pydantic import BaseModel

class AuthUserScheme(BaseModel):
    login: str
    password: str