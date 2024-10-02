LOGON_SUFFIXES = [
    "DEL",
    "RMP",
    "GND",
    "TWR",
    "DEP",
    "APP",
    "CTR",
    "FSS",
    "RDO",
    "TMV",
    "FMP",
]


def logon_validator(value: str) -> str:
    value = value.strip().upper()

    parts = value.split("_")

    if len(parts) >= 2 and not parts[-1] in LOGON_SUFFIXES:
        raise ValueError(f"Suffix {parts[-1]} is not allowed.")

    return value
