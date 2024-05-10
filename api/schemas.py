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

class DepartmentModel(BaseModel):
    name: str = Field(..., description="The name of the department")
    description: Optional[str] = Field(None, description="The description of the department")
    created_at: Optional[int] = Field(None, description="The creation time of the department")
    updated_at: Optional[int] = Field(None, description="The last update time of the department")

    class Config:
        orm_mode = True

class ProductModel(BaseModel):
    product_name: str = Field(..., description="The name of the product")
    product_description: Optional[str] = Field(None, description="The description of the product")
    buy_price: float = Field(..., description="The buying price of the product")
    sale_price: float = Field(..., description="The selling price of the product")
    stock: float = Field(..., description="The stock quantity of the product")
    department_id: int = Field(..., description="The ID of the department associated with the product")
    created_at: Optional[int] = Field(None, description="The creation time of the product")
    updated_at: Optional[int] = Field(None, description="The last update time of the product")

    class Config:
        orm_mode = True

class ProductGet(BaseModel):
    product_name: Optional[str] = Field(None, description="The name of the product")
    product_description: Optional[str] = Field(None, description="The description of the product")
    department_id: Optional[int] = Field(None, description="The ID of the department associated with the products")
    buy_price: Optional[float] = Field(None, description="The buying price of the product, if negative use <= else >=")
    sale_price: Optional[float] = Field(None, description="The selling price of the product, if negative use <= else >=")
    stock: Optional[float] = Field(None, description="The stock quantity of the product, if negative use <= else >=")

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
