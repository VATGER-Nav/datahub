import json


def createScheduleJson(inputFile, outputFile):
    try:
        with open(inputFile, "r") as json_file:
            json_array = json.load(json_file)

        minstation_dict = {}
        group_dict = {}

        MIL_STATION = "MIL"

        for element in json_array:
            # skip invalid elements
            if "logon" in element:
                logon = element["logon"]
            else:
                continue

            # populate schedule_show_always dict
            if "schedule_show_always" in element:
                min_stations = element["schedule_show_always"]
                for schedule_show_booked in min_stations:
                    if (
                        schedule_show_booked in minstation_dict
                        and logon not in group_dict[schedule_show_booked]
                    ):
                        minstation_dict[schedule_show_booked].append(logon)
                    else:
                        minstation_dict[schedule_show_booked] = [logon]

            # populate schedule_show_booked dict
            if "schedule_show_booked" in element:
                schedule_show_booked = element["schedule_show_booked"]
                for schedule_show_booked in schedule_show_booked:
                    if schedule_show_booked in group_dict:
                        group_dict[schedule_show_booked].append(logon)
                    else:
                        group_dict[schedule_show_booked] = [logon]

            # populate MIL stations, include all stations starting with "ET"
            if logon.startswith("ET"):
                # check if MIL_STATION key exists and logon does not exist in value list already
                if (
                    MIL_STATION in minstation_dict
                    and logon not in minstation_dict[MIL_STATION]
                ):
                    minstation_dict[MIL_STATION].append(logon)
                else:
                    minstation_dict[MIL_STATION] = [logon]

        grouped_data = {}

        # Group the data by keys
        for key in set(minstation_dict.keys()).union(group_dict.keys()):
            schedule_show_always = minstation_dict.get(key, [])
            schedule_show_booked = group_dict.get(key, [])

            grouped_data[key] = {
                "name": key,
                "schedule_show_always": schedule_show_always,
                "schedule_show_booked": schedule_show_booked,
            }

        # Convert the grouped data into a list of objects
        json_data = list(grouped_data.values())

        # sort the data by name key
        json_data.sort(key=lambda x: (x["name"]))

        # Export the JSON data to a file
        with open(outputFile, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

        print(f"Created schedule JSON in {outputFile}")

    except Exception as error:
        print("Error while creating schedule json", error)
