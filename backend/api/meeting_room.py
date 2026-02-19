from fastapi import APIRouter

from backend.crud.meeting_room import create_meeting_room
from backend.schemas.meeting_room import MeetingRoomCreate

router = APIRouter()


@router.post(
    '/meeting_rooms/',
    tags=['Переговорки'],
    summary='Создание переговорной комнаты саммари',
    description='Создание переговорной комнаты'
    )
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate,
):
    new_room = await create_meeting_room(meeting_room)
    return new_room
