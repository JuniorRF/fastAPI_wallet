from pydantic import BaseModel, Field, field_validator

from typing import Optional, Union
from enum import StrEnum


class EducationLevel(StrEnum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'


class Person(BaseModel):
    name: str = Field(
        ..., max_length=20,
        title='Полное имя',
        description='Можно вводить в любом регистре'
    )
    surname: Union[str, list[str]] = Field(..., max_length=50)
    age: Optional[int] = Field(None, gt=4, le=99)
    is_staff: bool = Field(False, alias='is-staff')
    education_level: Optional[EducationLevel]

    class Config:
        title = 'Класс для приветствия'
        str_min_length = 2

    
    @field_validator('name', 'surname')
    def name_cant_be_numeric(cls, value: str):
        if value.isnumeric():
            raise ValueError('Имя или Фамилия не может быть числом')
        return value