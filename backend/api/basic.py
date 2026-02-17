from fastapi import APIRouter, Query, File, Form, UploadFile, Body

from schemas.basic import Person


router = APIRouter()


@router.post('/login')
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


@router.post('/hello')
def hello(
    person: Person ) -> dict[str, str]:
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


@router.get('/')
def read_root() -> dict[str, str]:
    return {'Hello': 'FastAPI i HYI'}


@router.get(
    '/me',
    tags=['Инфо обо мне'],
    summary='Эндпоинт ME',
    description='Описание энпоинта'
    )
def hello_author() -> dict[str, str]:
    return {'Hello': 'author'}


@router.post('/{name}', response_description='Ответ: Нахуй')
def greetings(
        *,
        person: Person,
        cyrillic_string: str = Query('Здесь только кириллица', pattern='^[А-Яа-яЁё ]+$')
) -> dict[str, str]:
    """
    ## Описание эндпоинта)
    - с элементами
    - ```markdown```
    """
    result = ' '.join([person.name, person.surname])
    result = result.title()
    if person.age is not None:
        result += ', ' + str(person.age)
    if person.education_level is not None:
        result += ', ' + person.education_level.lower()
    if person.is_staff:
        result += ', сотрудник'
    return {'Hello': result}
