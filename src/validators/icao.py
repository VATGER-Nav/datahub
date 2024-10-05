import re


def icao_validator(icao: str) -> str:
    # strip whitespaces and force uppercase formatting
    icao = icao.strip().upper()

    if not re.match(r"^[A-Za-z]{4}$", icao):
        raise ValueError(f"Invalid ICAO code '{icao}'.")

    return icao
