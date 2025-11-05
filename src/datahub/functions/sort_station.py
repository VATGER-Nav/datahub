from typing import List

from datahub.validators.logon import LOGON_SUFFIXES
from datahub.views.station import Station


def sort_key(station: Station | dict):
    if isinstance(station, Station):
        parts = station.logon.split("_")
    else:
        parts = station.get("logon", "").split("_")

    prefix_order = parts[0]

    middlefix_sort = parts[1] if len(parts) > 1 else ""

    third_part = parts[2] if len(parts) > 2 else parts[1]

    # Map the third part using the LOGON_SUFFIXES order (missing part goes first)
    suffix_order = (
        LOGON_SUFFIXES.index(third_part) if third_part in LOGON_SUFFIXES else float("inf")
    )

    # sort by prefix, then suffix, then middlefix
    return (prefix_order, suffix_order, middlefix_sort)


def sort_stations(stations: List[Station]) -> List[Station]:
    """
    sorts the List of Station by its logon property
    sorting will be done first by its prefix, then its suffix and then its middlefix (if available)
    """
    return sorted(stations, key=sort_key)
