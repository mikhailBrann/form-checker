from pydantic import BaseModel

class UserAddSheme(BaseModel):
    name: str
    password: str
    email: str