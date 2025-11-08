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
        errors = []

        if exclude_folders is None:
            exclude_folders = set()

        for folder in data_dir.iterdir():
            if not folder.is_dir() or folder.name in exclude_folders:
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
                    errors.append((file_path, str(e)))

        # print errors
        if errors:
            logger.error("::group::Data validation summary")
            # create per-file annotation
            for file_path, err in errors:
                print(f"::error file={file_path},line=1::Validation or parsing failed: {err}")
            logger.error("::endgroup::")

            msg = f"DataLoader encountered {len(errors)} errors."
            raise RuntimeError(msg)

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
            msg = f"Failed to decode {file_path.suffix} file: {e}"
            raise ValueError(msg) from e
        except Exception as e:
            msg = f"Error reading file: {e}"
            raise ValueError(msg) from e

        if file_data is None:
            return []

        try:
            if isinstance(file_data, list):
                return [Station(**item) for item in file_data]
            else:
                return [Station(**file_data)]
        except ValidationError as e:
            msg = f"Validation error: {e}"
            raise ValueError(msg) from e
