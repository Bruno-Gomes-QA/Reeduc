from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from services import peopleServices as ps
from enum import Enum

class Status(Enum):
    Ativo = 'Ativo'
    Inativo = 'Inativo'

def get_people_types():
    response = ps.get_peoples_types()
    peoples = response.json()['data']
    peoples_types = {str(dept['id']): f"{dept['id']} - {dept['name'].upper()}" for dept in peoples}
    SelectPeoples = Enum('SelectionValue', peoples_types)
    return SelectPeoples

class PeopleModel(BaseModel):
    
    SelectPeople = get_people_types()

    name: str = Field(..., title='Nome')
    email: Optional[str] = Field(
        None, title='E-mail'
    )
    tel: Optional[str] = Field(
        None, title='Celular'
    )
    cpf: Optional[str] = Field(None, title='CPF')
    status: Status = Field(..., description='Status')
    if len(SelectPeople.__members__) > 0:
        people_type_id: SelectPeople = Field( # type: ignore
            list(SelectPeople)[0], title='Tipo de Pessoa'
        )
    else:
        people_type_id: str = Field( # type: ignore
            'Cadastre um Tipo Primeiro', title='Tipo de Pessoa'
    )