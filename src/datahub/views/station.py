from typing import Literal

from pydantic import BaseModel, field_validator

from datahub.validators.frequency import frequency_validator
from datahub.validators.icao import icao_validator
from datahub.validators.logon import logon_validator
from datahub.views.schedules import ScheduleType


class Station(BaseModel):
    logon: str
    frequency: str
    abbreviation: str
    description: str | None = None
    schedule_show_always: list[ScheduleType] | None = None
    schedule_show_booked: list[ScheduleType] | None = None
    relevant_airports: list[str] | None = None
    gcap_status: Literal["AFIS", "1", "2"] | None = None
    s1_twr: bool | None = None
    cpdlc_login: str | None = None
    s1_theory: bool | None = None

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
    def validate_frequency(cls, value: str) -> str:
        return frequency_validator(value)

    @field_validator("relevant_airports")
    @classmethod
    def validate_relevant_airports(cls, icao_list: list[str]) -> list[str] | None:
        if not icao_list or not isinstance(icao_list, list):
            return None

        if len(icao_list) == 0:
            return None

        return [icao_validator(element) for element in icao_list]

    @field_validator("schedule_show_booked", mode="before")
    @classmethod
    def filter_schedule_show_booked(cls, schedule_show_booked, info):
        """
        Remove entries from schedule_show_booked that are already in schedule_show_always.
        """
        schedule_show_always = info.data.get("schedule_show_always") or []

        # Filter out any entries from schedule_show_booked that are in schedule_show_always
        if schedule_show_booked:
            schedule_show_booked = [
                entry for entry in schedule_show_booked if entry not in schedule_show_always
            ]

        return schedule_show_booked

    @field_validator("cpdlc_login")
    @classmethod
    def validate_cpdlc_login(cls, value: str | None) -> str | None:
        if value is not None and len(value) != 4:
            msg = "cpdlc_login must be exactly 4 characters"
            raise ValueError(msg)
        return value
