from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DepartmentModel(BaseModel):
    name: str = Field(..., title='Nome do Departamento')
    description: Optional[str] = Field(
        None, title='Descrição do Departamento'
    )
