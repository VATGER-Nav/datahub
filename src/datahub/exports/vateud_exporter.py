import csv
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import requests
from bs4 import BeautifulSoup

from datahub.views.data_source import DataSource

if TYPE_CHECKING:
    from datahub.views.station import Station


@dataclass
class VateudStation:
    country_id: str
    callsign: str
    name: str
    frequency: str
    airport_region: str


class VateudExporter:
    @staticmethod
    def export(file_path: Path | str, data: list[DataSource]):
        stations: list[Station] = [station for ds in data for station in ds.data]

        vateud_stations_exclude_rules = [
            lambda s: s.country_id != "2",
            lambda s: not s.callsign.startswith(("ED", "ET")),
            lambda s: s.callsign.endswith("ATIS"),
        ]

        vateud_stations = VateudExporter._get_vateud_stations(vateud_stations_exclude_rules)
        print(f"Fetched {len(vateud_stations)} VATEUD stations")

        station_map = {s.logon: s for s in stations}
        vateud_map = {vs.callsign: vs for vs in vateud_stations}

        station_callsigns = set(station_map)
        vateud_callsigns = set(vateud_map)

        missing_in_vateud = station_callsigns - vateud_callsigns
        missing_in_stations = vateud_callsigns - station_callsigns

        csv_path = Path(file_path)
        csv_path.parent.mkdir(parents=True, exist_ok=True)

        with Path.open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([
                "Callsign (old)",
                "Name (old)",
                "Frequency (old)",
                "Callsign (new)",
                "Name (new)",
                "Frequency (new)",
                "Remark",
            ])

            for callsign in missing_in_vateud:
                s = station_map[callsign]
                writer.writerow([
                    "",
                    "",
                    "",
                    s.logon,
                    s.description or "",
                    s.frequency or "",
                    "Missing in VATEUD",
                ])

            for callsign in missing_in_stations:
                vs = vateud_map[callsign]
                writer.writerow([
                    vs.callsign,
                    vs.name,
                    vs.frequency,
                    "",
                    "",
                    "",
                    "Missing in Stations",
                ])

        print(f"CSV written to {csv_path}")

    @staticmethod
    def _get_vateud_stations(
        exclude_rules: list[Callable[[VateudStation], bool]] | None = None,
    ) -> list[VateudStation]:
        url = "https://fsmine.dhis.org/vateud8"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find_all("table")[1]
        rows = table.find_all("tr")[1:]

        stations = []

        for row in rows:
            cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
            if len(cells) < 5:
                continue

            station = VateudStation(cells[0], cells[1], cells[2], cells[3], cells[4])

            if exclude_rules and any(rule(station) for rule in exclude_rules):
                continue

            stations.append(station)

        return stations
