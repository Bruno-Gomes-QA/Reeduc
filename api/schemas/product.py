from pydantic import BaseModel, Field
from typing import Optional


class ProductModel(BaseModel):
    product_name: str = Field(..., description='The name of the product')
    product_description: Optional[str] = Field(
        None, description='The description of the product'
    )
    buy_price: float = Field(
        ..., description='The buying price of the product'
    )
    sale_price: float = Field(
        ..., description='The selling price of the product'
    )
    stock: float = Field(..., description='The stock quantity of the product')
    department_id: int = Field(
        ..., description='The ID of the department associated with the product'
    )
    created_at: Optional[int] = Field(
        None, description='The creation time of the product'
    )
    updated_at: Optional[int] = Field(
        None, description='The last update time of the product'
    )

    class Config:
        orm_mode = True


class ProductGet(BaseModel):
    product_name: Optional[str] = Field(
        None, description='The name of the product'
    )
    product_description: Optional[str] = Field(
        None, description='The description of the product'
    )
    department_id: Optional[int] = Field(
        None,
        description='The ID of the department associated with the products',
    )
    buy_price: Optional[float] = Field(
        None,
        description='The buying price of the product, if negative use <= else >=',
    )
    sale_price: Optional[float] = Field(
        None,
        description='The selling price of the product, if negative use <= else >=',
    )
    stock: Optional[float] = Field(
        None,
        description='The stock quantity of the product, if negative use <= else >=',
    )
