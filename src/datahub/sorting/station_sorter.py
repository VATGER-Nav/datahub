from datahub.validators.logon import LOGON_SUFFIXES
from datahub.views.data_source import DataSource
from datahub.views.station import Station


class StationSorter:
    @staticmethod
    def sort(source: DataSource | list[DataSource]):
        # list data source objects
        if isinstance(source, list) and source and isinstance(source[0], DataSource):
            for ds in source:
                ds.data = StationSorter.sort(ds.data)
            return source
        # single data source object
        elif isinstance(source, DataSource):
            source.data = StationSorter.sort(source.data)
            return source
        # list of stations
        elif isinstance(source, list) and (not source or isinstance(source[0], Station)):
            return StationSorter.sort_stations(source)
        # unsupported types:
        elif isinstance(source, list) and not source:
            return []
        else:
            msg = f"Unsupported input type for sorting: {type(source)}"
            raise TypeError(msg)

    @staticmethod
    def sort_key(station):
        logon = StationSorter.get_logon(station)
        parts = logon.split("_")

        prefix = parts[0] if len(parts) > 0 else ""
        middle = parts[1] if len(parts) > 1 else ""
        third = parts[2] if len(parts) > 2 else parts[1] if len(parts) > 1 else ""

        suffix_order = LOGON_SUFFIXES.index(third) if third in LOGON_SUFFIXES else float("inf")

        return (prefix, suffix_order, middle)

    @staticmethod
    def get_logon(value):
        # callsign directly
        if isinstance(value, str):
            return value

        if isinstance(value, dict):
            return value.get("logon", "")

        if hasattr(value, "logon"):
            return value.logon

        msg = f"Cannot extract logon from type {type(value)}"
        raise TypeError(msg)

    @staticmethod
    def sort_stations(stations: list[Station]) -> list[Station]:
        return sorted(stations, key=StationSorter.sort_key)
