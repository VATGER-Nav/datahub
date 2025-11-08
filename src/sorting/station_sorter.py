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
    def sort_key(station: Station | dict):
        if isinstance(station, Station):
            parts = station.logon.split("_")
        else:
            parts = station.get("logon", "").split("_")

        prefix_order = parts[0]

        middlefix_sort = parts[1] if len(parts) > 1 else ""

        third_part = parts[2] if len(parts) > 2 else parts[1]

        # map the third part using the LOGON_SUFFIXES order (missing part goes first)
        suffix_order = (
            LOGON_SUFFIXES.index(third_part) if third_part in LOGON_SUFFIXES else float("inf")
        )

        # sort by prefix, then suffix, then middlefix
        return (prefix_order, suffix_order, middlefix_sort)

    @staticmethod
    def sort_stations(stations: list[Station]) -> list[Station]:
        return sorted(stations, key=StationSorter.sort_key)
