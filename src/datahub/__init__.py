from pathlib import Path

from datahub.exports.data_exporter import DataExporter
from datahub.exports.schedule_exporter import ScheduleExporter
from datahub.exports.ts_exporter import TeamspeakExporter
from datahub.loaders.data_loader import DataLoader
from sorting.station_sorter import StationSorter

DATA_DIR = Path("data/")
API_DIR = Path("api/")


def check_data():
    DataLoader.load(DATA_DIR, exclude_folders={"event_schedules", "topsky"})


def combine_data():
    data = DataLoader.load(DATA_DIR, exclude_folders={"event_schedules", "topsky"})

    data = StationSorter.sort(data)

    DataExporter.export(API_DIR, data, combine=True)
    TeamspeakExporter.export(API_DIR / "legacy/atc_station_mappings.json", data)
    ScheduleExporter.export(API_DIR / "legacy/schedule.json", data)


def sort_data():
    data = DataLoader.load(DATA_DIR, exclude_folders={"event_schedules", "topsky"})

    data = StationSorter.sort(data)

    DataExporter.export(DATA_DIR, data)
