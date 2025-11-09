import json
from pathlib import Path

import toml

from datahub.settings import JSON_INDENT
from datahub.views.data_source import DataSource
from sorting.station_sorter import StationSorter


class DataExporter:
    @staticmethod
    def export(
        folder_path: str | Path,
        data: list[DataSource],
        combine: bool = False,
        target_format: str | None = None,
    ):
        folder_path = Path(folder_path)

        combined_data = []

        for file in data:
            original_path = Path(file.source)
            file_path = folder_path / original_path

            if target_format:
                file_path = file_path.with_suffix(f".{target_format}")

            file_path.parent.mkdir(parents=True, exist_ok=True)

            if combine:
                combined_data.extend(file.data)

            stations_data = [station.to_dict() for station in file.data]

            if file_path.suffix == ".json":
                with file_path.open("w", encoding="utf-8") as f:
                    json.dump(stations_data, f, indent=JSON_INDENT, ensure_ascii=False)
            elif file_path.suffix == ".toml":
                with file_path.open("w", encoding="utf-8") as f:
                    toml.dump({"stations": stations_data}, f)
            else:
                msg = f"Unsupported file extension: {file_path.suffix}"
                raise ValueError(msg)

        if combine:
            combined_path = folder_path / f"stations.{target_format or 'json'}"

            combined_data = StationSorter.sort(combined_data)
            serializable_data = [s.to_dict() for s in combined_data]

            with combined_path.open("w", encoding="utf-8") as f:
                if (target_format or "json") == "json":
                    json.dump(serializable_data, f, indent=JSON_INDENT, ensure_ascii=False)
                else:
                    toml.dump({"stations": serializable_data}, f)
