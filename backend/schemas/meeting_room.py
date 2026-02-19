from typing import Optional

from pydantic import BaseModel, Field


class MeetingRoomCreate(BaseModel):
    name: str = Field(
        ..., max_length=20,
        title='Название переговорной',
        description='Описание переговорной'
    )
    description: Optional[str]
