from pydantic import BaseModel

class UserPubSheme(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True