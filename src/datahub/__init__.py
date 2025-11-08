from pathlib import Path

from datahub.classes.datahub import Datahub
from datahub.loaders.data_loader import DataLoader
from sorting.station_sorter import StationSorter

DATA_DIR = Path("data/")


def check_data():
    DataLoader.load(DATA_DIR, exclude_folders={"event_schedules", "topsky"})


def combine_data():
    Datahub().combine_data()


def sort_data():
    data = DataLoader.load(DATA_DIR, exclude_folders={"event_schedules", "topsky"})

    data = StationSorter.sort(data)

    Datahub().sort_data()
