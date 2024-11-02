from dataclasses import dataclass
import os
import json
from pydantic import BaseModel
import toml
from typing import List, Literal

from functions.sort_station import sort_stations
from settings.json import JSON_INDENT
from views.station import Station


@dataclass
class Data:
    source: str
    data: List[Station]


class Datahub:
    def __init__(
        self,
        data_dir="data",
        station_dirs=None,
        event_dir="event_schedules",
    ):
        self.data_dir = data_dir
        if not station_dirs:
            self.station_dirs = ["edgg", "edww", "edmm", "edyy", "eduu", "edxx"]
        self.event_dir = event_dir

        self.data: List[Data] = []
        self.combined_file_name = "stations"

        self.teamspeak_mapping_path = "api/legacy/atc_station_mappings.json"

    def sort_data(self):
        """reads the data, sorts it, exports it back to the files it originates from"""

        self.__read_data()

        for file in self.data:
            file.data = sort_stations(file.data)

        self.__export(self.data, destination="data")

        return self

    def check_data(self):
        """The functions which handles data validation"""

        self.__read_data()

        # TODO: currently Station validation is implemented using Pydantic's type validation
        # so there is currently no further validation required
        # maybe later we can validate event_schedules.json

    def combine_data(self):
        """combines the data and exports it at into the "api" folder"""
        self.__read_data()
        self.__export(self.data, destination="api", combine=True)

        self.__generate_teamspeak_mapping_file()
        # TODO: generate schedules.json
        # TODO: move event_schedules.json

    def __generate_teamspeak_mapping_file(self):
        mapping_data = []

        for file in self.data:
            for station in file.data:
                callsign_parts = station.logon.split("_")
                callsign_prefix = callsign_parts[0] if callsign_parts else ""

                station_mapping = {
                    "id": station.abbreviation,
                    "callsignPrefix": callsign_prefix,
                    "frequency": station.frequency,
                }

                mapping_data.append(station_mapping)

        # Sort mapping_data by 'callsignPrefix' first, then by 'id'
        mapping_data.sort(key=lambda x: (x["callsignPrefix"], x["id"]))

        with open(
            self.teamspeak_mapping_path, "w", encoding="utf-8"
        ) as output_json_file:
            json.dump(mapping_data, output_json_file, indent=JSON_INDENT)

    def __export(
        self,
        data: List[Data],
        destination: Literal["data", "api"] = "data",
        combine=False,
    ):
        """exports data back to data/* or api/*"""

        combined_data = []

        for element in data:
            file_path = element.source
            if file_path.startswith("data") and destination == "api":
                file_path = file_path.replace("data", destination, 1)
                folder_path = os.path.dirname(file_path)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

            stations_data = [station.to_dict() for station in element.data]

            if file_path.endswith(".json"):
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(stations_data, f, indent=JSON_INDENT)
                    print(f"Data written to {file_path} as JSON.")
            elif file_path.endswith(".toml"):
                with open(file_path, "w", encoding="utf-8") as f:
                    toml.dump({"stations": stations_data}, f)
                    print(f"Data written to {file_path} as TOML.")

            if combine:
                combined_data.extend(element.data)

        if combine:
            file_path = destination + "/" + self.combined_file_name + ".json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(stations_data, f, indent=JSON_INDENT)

    def __read_data(self):
        """reads and parses all data from data/*"""
        for folder in self.station_dirs:
            folder_path = os.path.join(self.data_dir, folder)
            if os.path.exists(folder_path):
                self.__parse_folder(folder_path)

    def __parse_folder(self, folder_path):
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".json") or file.endswith(".toml"):
                    file_path = os.path.join(root, file)
                    self.__parse_file(file_path)

    def __parse_file(self, file_path):
        file_data = None
        if file_path.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as json_file:
                file_data = json.load(json_file)

        if file_path.endswith(".toml"):
            with open(file_path, "r", encoding="utf-8") as toml_file:
                file_data = toml.load(toml_file)

        data = self.__parse_data(file_data)

        if len(data) != 0:
            self.data.append(Data(source=file_path, data=data))

    def __parse_data(self, file_data):
        if not file_data:
            return []

        stations = []
        for element in file_data:
            stations.append(Station.from_dict(element))

        return stations
