from datetime import datetime, timedelta

from pydantic import BaseModel, Field, field_validator, model_validator


class ReservationBase(BaseModel):
    reservation_start: datetime = Field(
        default=datetime.now(),
        title="Начало времени бронирования",
        description="Начало времени бронирования"
    )
    to_reserve: datetime = Field(
        default=datetime.now() + timedelta(minutes=30),
        title="Конец времени бронирования",
        description="Конец времени бронирования"
    )


class ReservationUpdate(ReservationBase):

    @field_validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value):
        if value <= datetime.now():
            raise ValueError(
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
        return value

    @model_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if values['from_reserve'] >= values['to_reserve']:
            raise ValueError(
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
        return values

    @field_validator('reservation_start')
    def reservation_start_cannot_be_null(cls, value):
        if value is None or value == '':
            raise ValueError(
                'Время резарвации переговорки не может быть пустым!')
        return value


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int

    class Config:
        from_attributes = True
