from pydantic import BaseModel, Field
from typing import Optional


class UserModel(BaseModel):
    name: str = Field(..., description='Type name this User')
    email: str = Field(..., description='The email this User')
    tel: Optional[str] = Field(
        None, description='The telephone number of the User'
    )
    password: str = Field(..., description='Encrypted password of the User')
    created_at: Optional[int] = Field(
        None, description='The creation time of the person'
    )
    updated_at: Optional[int] = Field(
        None, description='The last update time of the person'
    )

    class Config:
        orm_mode = True


class UserGet(BaseModel):
    name: Optional[str] = Field(None, description='The name of the User')
    email: Optional[str] = Field(None, description='The email of the User')
    tel: Optional[str] = Field(
        None, description='The telephone number of the User'
    )

    class Config:
        orm_mode = True
