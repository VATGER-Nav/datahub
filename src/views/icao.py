from pydantic import BaseModel, Field, field_validator


class ICAO(BaseModel):
    icao: str = Field(
        ...,
        pattern=r"^[A-Za-z]{4}$",
        description="Must be a string of exactly 4 letters.",
    )

    @field_validator("icao")
    @classmethod
    def validate_icao(cls, value: str) -> str:
        return value.strip().upper()
