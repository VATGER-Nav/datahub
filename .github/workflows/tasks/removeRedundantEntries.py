import os
import json
import sys


def removeRedundantScheduleEntries(folders):
    print("Removing redundant entries: ")
    for folder in folders:
        for filename in os.listdir(folder):
            if not filename.endswith(".json"):
                continue
            file_path = os.path.join(folder, filename)
            try:
                with open(file_path, "r") as json_file:
                    data = json.load(json_file)

                for element in data:
                    if (
                        not "schedule_show_always" in element
                        or not "schedule_show_booked" in element
                    ):
                        continue

                    schedule_show_always = element["schedule_show_always"]
                    schedule_show_booked = element["schedule_show_booked"]

                    # Create a new list for schedule_show_booked without redundant entries
                    new_schedule_show_booked = [
                        group
                        for group in schedule_show_booked
                        if group not in schedule_show_always
                    ]

                    if new_schedule_show_booked != schedule_show_booked:
                        print(
                            "Removed:",
                            [
                                group
                                for group in schedule_show_booked
                                if group not in new_schedule_show_booked
                            ],
                            "from",
                            element["logon"],
                        )

                    if not new_schedule_show_booked:
                        del element[
                            "schedule_show_booked"
                        ]  # Remove the key if the list is empty
                    else:
                        element["schedule_show_booked"] = (
                            new_schedule_show_booked  # Update with the new list
                        )

                with open(file_path, "w") as json_file:
                    json.dump(data, json_file, indent=2)

            except json.JSONDecodeError as e:
                print(f"Error loadig JSON from {file_path}: {e}")
                sys.exit(1)

    print("\n\n\n")
