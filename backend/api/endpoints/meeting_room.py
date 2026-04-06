from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.endpoints.validators import (
    check_meeting_room_exists, check_name_duplicate)
from backend.core.db import get_async_session
from backend.core.user import current_superuser
from backend.crud.meeting_room import meeting_room_crud
from backend.crud.reservation import reservation_crud
from backend.schemas.meeting_room import (
    MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
)
from backend.schemas.reservation import ReservationDB

router = APIRouter()


@router.post(
    '/',
    summary='Создание переговорной комнаты саммари',
    description='Создание переговорной комнаты',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    )
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        new_room = await meeting_room_crud.create(meeting_room, session)
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
    return await meeting_room_crud.get_multi(session)


@router.patch(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
        meeting_room_id: int,
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room


@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_meeting_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для Администратора сисьемы"""
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    meeting_room = await meeting_room_crud.remove(
        meeting_room, session
    )
    return meeting_room


@router.get(
    '/{meeting_room_id}/reservations',
    response_model=List[ReservationDB],
    )
async def get_reservations_for_room(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    await check_meeting_room_exists(
        meeting_room_id, session
    )
    reservations = await reservation_crud.get_future_reservations_for_room(
        meeting_room_id, session
        )
    return reservations
