from pydantic import BaseModel, Field
from typing import Optional

class PeopleModel(BaseModel):
    name: str = Field(..., description='The name of the person')
    email: Optional[str] = Field(
        None, description='The email address of the person'
    )
    tel: Optional[str] = Field(
        None, description='The telephone number of the person'
    )
    cpf: str = Field(None, description='The CPF of the person')
    status: int = Field(..., description='The status of the person')
    people_type_id: int = Field(
        ..., description='The ID of the people type associated with the person'
    )
    created_at: Optional[int] = Field(
        None, description='The creation time of the person'
    )
    updated_at: Optional[int] = Field(
        None, description='The last update time of the person'
    )

    class Config:
        orm_mode = True

class PeopleGet(BaseModel):
    name: Optional[str] = Field(
        None, description='The name of the person'
    )
    email: Optional[str] = Field(
        None, description='The email of the person'
    )
    tel: Optional[str] = Field(
        None, description='The telephone number of the person'
    )
    cpf: Optional[str] = Field(
        None, description='The CPF of the person'
    )
    status: Optional[int] = Field(
        None, description='The status of the person'
    )
    people_type_id: Optional[int] = Field(
        None, description='The ID of the people type associated with the person'
    )

    class Config:
        orm_mode = True

class PeopleTypeModel(BaseModel):
    name: str = Field(..., description='The type of person')
    description: Optional[str] = Field(
        None, description='The description of the person type'
    )
    created_at: Optional[int] = Field(
        None, description='The creation time of the person type'
    )
    updated_at: Optional[int] = Field(
        None, description='The last update time of the person type'
    )
    class Config:
        orm_mode = True