from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.crud.meeting_room import (
    create_meeting_room, read_all_rooms_from_db,
    get_meeting_room_by_id, get_room_id_by_name,
    update_meeting_room, delete_meeting_room
    )
from backend.schemas.meeting_room import (
    MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
)

router = APIRouter(
    prefix='/meeting_rooms',
    tags=['Переговорки']
)


@router.post(
    '/',
    summary='Создание переговорной комнаты саммари',
    description='Создание переговорной комнаты',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    )
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        new_room = await create_meeting_room(meeting_room, session)
        return new_room
    except Exception:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )


@router.get(
    '/',
    summary='Получение всех переговорных комнат',
    description='Получение всех переговорных комнат',
    response_model=List[MeetingRoomDB],
    response_model_exclude_none=True,
    response_model_exclude_defaults=True,
    )
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session)
):
    return await read_all_rooms_from_db(session)


@router.post('/update')
async def update_meeting_rooms(
    room_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_meeting_room_by_id(room_id, session)


@router.patch(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def partially_update_meeting_room(
        meeting_room_id: int,
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    meeting_room = await update_meeting_room(
        meeting_room, obj_in, session
    )
    return meeting_room


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    room_id = await get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорка с таким именем уже существует!',
        )


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def remove_meeting_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    meeting_room = await delete_meeting_room(
        meeting_room, session
    )
    return meeting_room


async def check_meeting_room_exists(
        meeting_room_id: int,
        session: AsyncSession,
) -> MeetingRoomDB:
    meeting_room = await get_meeting_room_by_id(
        meeting_room_id, session
    )
    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорка не найдена!'
        )
    return meeting_room
