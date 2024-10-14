from typing import List, Literal
from pydantic import BaseModel, field_validator

from validators.icao import icao_validator
from validators.logon import logon_validator
from validators.frequency import frequency_validator
from views.schedules import ScheduleType


class Station(BaseModel):
    logon: str
    frequency: str
    abbreviation: str
    description: str | None
    schedule_show_always: List[ScheduleType] | None
    schedule_show_booked: List[ScheduleType] | None
    relevant_airports: List[str] | None
    gcap_status: Literal["AFIS", "1", "2", None]
    s1_twr: bool | None

    @classmethod
    def from_dict(cls, data: dict) -> "Station":
        return Station(
            logon=data.get("logon"),
            frequency=data.get("frequency"),
            abbreviation=data.get("abbreviation"),
            description=data.get("description"),
            schedule_show_always=data.get("schedule_show_always"),
            schedule_show_booked=data.get("schedule_show_booked"),
            relevant_airports=data.get("relevant_airports"),
            gcap_status=data.get("gcap_status"),
            s1_twr=data.get("s1_twr"),
        )

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)

    @field_validator("logon")
    @classmethod
    def validate_logon(cls, value: str) -> str:
        return logon_validator(value)

    @field_validator("frequency")
    @classmethod
    def validate_frequency(cls, value: float) -> float:
        return frequency_validator(value)

    @field_validator("relevant_airports")
    @classmethod
    def validate_relevant_airports(cls, icao_list: List[str]) -> List[str]:
        if not icao_list:
            return

        for element in icao_list:
            element = icao_validator(element)
