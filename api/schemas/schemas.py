from pydantic import BaseModel, Field
from typing import Optional


class AccountModel(BaseModel):
    account_type: str = Field(..., description='The type of the account')
    account_name: str = Field(..., description='The name of the account')
    account_description: Optional[str] = Field(
        None, description='The description of the account'
    )
    balance: float = Field(
        ..., description='The current balance of the account'
    )
    created_at: Optional[int] = Field(
        None, description='The creation time of the account'
    )
    updated_at: Optional[int] = Field(
        None, description='The last update time of the account'
    )

    class Config:
        orm_mode = True
