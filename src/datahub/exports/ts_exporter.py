import json
import operator
from pathlib import Path

from datahub.settings import JSON_INDENT
from datahub.views.data_source import DataSource


class TeamspeakExporter:
    @staticmethod
    def export(folder_path: Path | str, data: list[DataSource]):
        folder_path = Path(folder_path)
        mapping_data = []

        for file in data:
            for station in file.data:
                callsign_parts = station.logon.split("_")
                callsign_prefix = callsign_parts[0] if callsign_parts else ""

                station_mapping = {
                    "id": station.abbreviation,
                    "callsignPrefix": callsign_prefix,
                    "frequency": station.frequency,
                }

                mapping_data.append(station_mapping)

        # sort mapping_data by 'callsignPrefix' first, then by 'id'
        mapping_data.sort(key=operator.itemgetter("callsignPrefix", "id"))

        folder_path.parent.mkdir(parents=True, exist_ok=True)

        with Path.open(folder_path, "w+", encoding="utf-8") as output_json_file:
            json.dump(mapping_data, output_json_file, indent=JSON_INDENT)

        print(f"TeamspeakExporter: exported {len(mapping_data)} stations")
