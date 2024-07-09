from pydantic import BaseModel, Field
from typing import Optional, Set
from enum import Enum
from services import departmentServices as ds


def get_departments():
    response = ds.get_departments()
    departments = response.json()['data']
    department_names = {str(dept['id']): f"{dept['id']} - {dept['name'].upper()}" for dept in departments}
    SelectDepartments = Enum('SelectionValue', department_names)
    return SelectDepartments

class ProductModel(BaseModel):

    SelectDepartments = get_departments()

    product_name: str = Field(..., title='Nome do Produto')
    product_description: Optional[str] = Field(
        None, title='Descrição do Produto'
    )
    buy_price: float = Field(
        ..., title='Preço de Compra'
    )
    sale_price: float = Field(
        ..., title='Preço de Venda'
    )
    if len(SelectDepartments.__members__) > 0:
        department_id: SelectDepartments = Field( # type: ignore
            list(SelectDepartments)[0], title='Departamento do Produto'
        )
    else:
        department_id: str = Field( # type: ignore
            'Cadastre um Departamento Primeiro', title='Departamento do Produto'
    )
    stock: float = Field(..., title='Estoque')


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
