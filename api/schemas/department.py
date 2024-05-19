from pydantic import BaseModel, Field
from typing import Optional


class DepartmentModel(BaseModel):
    name: str = Field(..., description='The name of the department')
    description: Optional[str] = Field(
        None, description='The description of the department'
    )
    created_at: Optional[int] = Field(
        None, description='The creation time of the department'
    )
    updated_at: Optional[int] = Field(
        None, description='The last update time of the department'
    )

    class Config:
        orm_mode = True
