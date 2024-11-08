from typing import List, Literal
from pydantic import BaseModel, ValidationInfo, field_validator

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
    cpdlc_login: str | None = None

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
            cpdlc_login=data.get("cpdlc_login"),
        )

    def to_dict(self) -> dict:
        """returns the station as dict, hides fields which are None or empty lists"""
        data = self.model_dump(exclude_none=True)
        return {k: v for k, v in data.items() if v != []}

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

    @field_validator("schedule_show_booked", mode="before")
    @classmethod
    def filter_schedule_show_booked(cls, schedule_show_booked, values):
        """
        Remove entries from schedule_show_booked that are already in schedule_show_always.
        """
        schedule_show_always = values.data.get("schedule_show_always") or []

        # Filter out any entries from schedule_show_booked that are in schedule_show_always
        if schedule_show_booked:
            schedule_show_booked = [
                entry
                for entry in schedule_show_booked
                if entry not in schedule_show_always
            ]

        return schedule_show_booked

    @field_validator("cpdlc_login")
    @classmethod
    def validate_length(cls, value):
        if value is not None and len(value) != 4:
            raise ValueError("cpdlc_login must be exactly 4 characters")
        return value
