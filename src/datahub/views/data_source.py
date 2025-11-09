from dataclasses import dataclass

from datahub.views.station import Station


@dataclass
class DataSource:
    source: str
    data: list[Station]
