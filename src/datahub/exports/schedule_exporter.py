import json
import operator
from pathlib import Path

from datahub.settings import JSON_INDENT
from datahub.views.data_source import DataSource


class ScheduleExporter:
    @staticmethod
    def export(schedule_path: Path | str, data: list[DataSource]):
        inverted_schedule: list[dict[str, list[str]]] = []

        schedule_types = ["EDGG", "EDMM", "EDWW", "MIL"]

        for schedule_type in schedule_types:
            schedule_entry = {
                "name": schedule_type,
                "schedule_show_always": [],
                "schedule_show_booked": [],
            }

            for file in data:
                for station in file.data:
                    # mil stations:
                    if station.logon.startswith("ET") and schedule_type == "MIL":
                        if station.schedule_show_always:
                            schedule_entry["schedule_show_always"].append(station.logon)
                        if station.schedule_show_booked:
                            schedule_entry["schedule_show_booked"].append(station.logon)

                    if (
                        station.schedule_show_always
                        and schedule_type in station.schedule_show_always
                    ):
                        schedule_entry["schedule_show_always"].append(station.logon)
                    if (
                        station.schedule_show_booked
                        and schedule_type in station.schedule_show_booked
                    ):
                        schedule_entry["schedule_show_booked"].append(station.logon)

            schedule_entry["schedule_show_always"].sort()
            schedule_entry["schedule_show_booked"].sort()

            inverted_schedule.append(schedule_entry)

        inverted_schedule.sort(key=operator.itemgetter("name"))

        print(f"ScheduleExporter: exported {len(inverted_schedule)} schedules")

        with Path.open(schedule_path, "w", encoding="utf-8") as output_json_file:
            json.dump(inverted_schedule, output_json_file, indent=JSON_INDENT)
