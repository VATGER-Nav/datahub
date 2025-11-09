import json
import operator
from pathlib import Path

from datahub.views.data_source import DataSource


class TopskyExporter:
    @staticmethod
    def export(
        schedule_path: Path | str,
        data: list[DataSource],
        cpdlc_mapping=Path("data/topsky/cpdlcMap.json"),
    ):
        cpdlc_callsign_map = json.load(Path.open(cpdlc_mapping, "r", encoding="utf-8"))

        cpdlc_station_data = []

        for file in data:
            for station in file.data:
                if not station.cpdlc_login:
                    continue

                callsign = cpdlc_callsign_map.get(station.logon.split("_")[0])

                cpdlc_station_data.append({
                    "login": station.cpdlc_login,
                    "callsign": callsign,
                    "abbreviation": station.abbreviation,
                })

        # sort data by callsign then by login
        cpdlc_station_data.sort(key=operator.itemgetter("callsign", "login"))

        output_lines = []
        last_callsign = cpdlc_station_data[0]["callsign"]

        for station in cpdlc_station_data:
            # Add an empty line after every change of callsign
            if station["callsign"] != last_callsign:
                output_lines.append("\n")

            output_lines.append(
                f"LOGIN:{station['login']}:{station['callsign']}:{station['abbreviation']}\n"
            )

            last_callsign = station["callsign"]

        print(f"TopskyExporter: exported {len(cpdlc_station_data)} stations")

        with Path.open(schedule_path, "w", encoding="utf-8") as output_text:
            output_text.writelines(output_lines)
