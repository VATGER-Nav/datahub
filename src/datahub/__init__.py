from pathlib import Path

from datahub.classes.datahub import Datahub
from datahub.loaders.data_loader import DataLoader

DATA_DIR = Path("data/")


def check_data():
    DataLoader.load(DATA_DIR, exclude_folders={"event_schedules", "topsky"})


def combine_data():
    Datahub().combine_data()


def sort_data():
    Datahub().sort_data()
