from typing import Optional

from pydantic import BaseModel, Field, validator


class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=20,
        title='Название переговорной',
        description='Описание переговорной'
    )
    description: Optional[str] = None


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(
        ...,
        max_length=20,
        title='Название переговорной',
        description='Описание переговорной'
    )


class MeetingRoomDB(MeetingRoomCreate):
    id: int

    class Config:
        from_attributes = True


class MeetingRoomUpdate(MeetingRoomBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value
