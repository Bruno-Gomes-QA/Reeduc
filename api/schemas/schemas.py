from pydantic import BaseModel, Field
from typing import Optional

class AccountModel(BaseModel):
    account_type: str = Field(..., description="The type of the account")
    account_name: str = Field(..., description="The name of the account")
    account_description: Optional[str] = Field(None, description="The description of the account")
    balance: float = Field(..., description="The current balance of the account")
    created_at: Optional[int] = Field(None, description="The creation time of the account")
    updated_at: Optional[int] = Field(None, description="The last update time of the account")

    class Config:
        orm_mode = True

class PeopleModel(BaseModel):
    name: str = Field(..., description="The name of the person")
    email: Optional[str] = Field(None, description="The email address of the person")
    tel: Optional[str] = Field(None, description="The telephone number of the person")
    cpf: Optional[str] = Field(None, description="The CPF of the person")
    status: int = Field(..., description="The status of the person")
    people_type_id: int = Field(..., description="The ID of the people type associated with the person")
    created_at: Optional[int] = Field(None, description="The creation time of the person")
    updated_at: Optional[int] = Field(None, description="The last update time of the person")

    class Config:
        orm_mode = True
