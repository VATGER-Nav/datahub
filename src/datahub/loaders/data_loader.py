import json
import logging
from pathlib import Path

import toml
from pydantic import ValidationError

from datahub.views.data_source import DataSource
from datahub.views.station import Station

logger = logging.getLogger(__name__)


class DataLoader:
    """Reads raw data from files"""

    @staticmethod
    def load(data_dir: Path | str, exclude_folders: set[str] | None = None) -> list[DataSource]:
        data_dir = Path(data_dir)
        data = []

        if exclude_folders is None:
            exclude_folders = set()

        for folder in data_dir.iterdir():
            if not folder.is_dir():
                continue

            if folder.name in exclude_folders:
                continue

            for file_path in folder.iterdir():
                if not file_path.is_file():
                    continue

                try:
                    stations = DataLoader._parse_file(file_path)

                    if stations:
                        relative_path = file_path.relative_to(data_dir)
                        data.append(DataSource(source=str(relative_path), data=stations))
                except Exception as e:  # noqa: BLE001
                    logger.warning(f"Failed to parse file {file_path}: {e}")

        return data

    @staticmethod
    def _parse_file(file_path: Path) -> list[Station]:
        """Parse a file and return list of stations"""
        file_data = None

        try:
            if file_path.suffix == ".json":
                with file_path.open("r") as f:
                    file_data = json.load(f)
            elif file_path.suffix == ".toml":
                with file_path.open("r") as f:
                    file_data = toml.load(f)
        except (json.JSONDecodeError, toml.TomlDecodeError) as e:
            logger.warning(f"Failed to decode {file_path.suffix} file {file_path}: {e}")
            return []
        except Exception as e:  # noqa: BLE001
            logger.warning(f"Error reading file {file_path}: {e}")
            return []

        if file_data is None:
            return []

        # handle both single station and list of stations
        try:
            if isinstance(file_data, list):
                return [Station(**item) for item in file_data]
            else:
                return [Station(**file_data)]
        except ValidationError as e:
            logger.warning(f"Validation error for {file_path}: {e}")
            return []
        except Exception as e:  # noqa: BLE001
            logger.warning(f"Error creating Station objects from {file_path}: {e}")
            return []
