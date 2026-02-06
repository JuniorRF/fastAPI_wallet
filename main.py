from fastapi import FastAPI, Query, File, Form, UploadFile
from pydantic import BaseModel
import uvicorn

from typing import Optional, Union
from enum import StrEnum


class EducationLevel(StrEnum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'


class Person(BaseModel):
    name: str
    surname: Union[str, list[str]]
    age: Optional[int]
    is_staff: bool = False
    education_level: Optional[EducationLevel]


app = FastAPI() #(docs_url=None, redoc_url=None)

@app.post('/login')
def login(
        username: str = Form(...),
        password: str = Form(...),
        some_file: UploadFile = File(...)
):
    file_content = some_file.file.read().splitlines()
    return {
        'username': username,
        'file_content': file_content
    } 


@app.post('/hello')
def hello(person: Person) -> dict[str, str]:
    if isinstance(person.surname, list):
        surnames = ' '.join(person.surname)
    else:
        surnames = person.surname
    result = ' '.join([person.name, surnames])
    result = result.title()    
    if person.age is not None:
        result += ', ' + str(person.age)
    if person.education_level is not None:
        result += ', ' + person.education_level.lower()
    if person.is_staff:
        result += ', сотрудник'
    return {'Hello': result} 


@app.get('/')
def read_root() -> dict[str, str]:
    return {'Hello': 'FastAPI i HYI'}


@app.get(
    '/me',
    tags=['Инфо обо мне'],
    summary='Эндпоинт ME',
    description='Описание энпоинта'
    )
def hello_author() -> dict[str, str]:
    return {'Hello': 'author'}


@app.get('/{name}', response_description='Ответ: Нахуй')
def greetings(
        *,
        age: Optional[int] = None,
        education_level: Optional[EducationLevel] = None,
        is_staff: bool = False,   
        name: str,
        surname: str,
        cyrillic_string: str = Query('Здесь только кириллица', regex='^[А-Яа-яЁё ]+$')
) -> dict[str, str]:
    """
    ## Описание эндпоинта)
    - с элементами
    - ```markdown```
    """
    result = ' '.join([name, surname])
    result = result.title()
    if age is not None:
        result += ', ' + str(age)
    if education_level is not None:
        result += ', ' + education_level.lower()
    if is_staff:
        result += ', сотрудник'
    return {'Hello': result} 


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
