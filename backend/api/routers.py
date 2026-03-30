from fastapi import APIRouter

from backend.api.endpoints import (
    meeting_room_router, reservation_router, user_router)


main_router = APIRouter()

main_router.include_router(
    meeting_room_router, prefix='/meeting_rooms', tags=['Переговорные комнаты']
)

main_router.include_router(
    reservation_router, prefix='/reservations',
    tags=['Бронирование переговорной']
)

main_router.include_router(user_router)
