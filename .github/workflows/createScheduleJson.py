import json

def createScheduleJson(inputFile, outputFile):
    try: 
        with open(inputFile, "r") as json_file:
            json_array = json.load(json_file)

        minstation_dict = {}
        group_dict = {}

        for element in json_array:
            # skip invalid elements
            if "logon" in element:
                 logon = element["logon"]
            else:
                continue
            
            # populate schedule_minstation dict
            if "schedule_minstation" in element:
                min_stations = element["schedule_minstation"]
                for schedule_group in min_stations:
                    if schedule_group in minstation_dict:
                        minstation_dict[schedule_group].append(logon)
                    else:
                         minstation_dict[schedule_group] = [logon]

            # populate schedule_group dict
            if "schedule_groups" in element:
                schedule_groups = element["schedule_groups"]
                for schedule_group in schedule_groups:
                    if schedule_group in group_dict:
                        group_dict[schedule_group].append(logon)
                    else:
                        group_dict[schedule_group] = [logon]

        grouped_data = {}

        # Group the data by keys
        for key in set(minstation_dict.keys()).union(group_dict.keys()):
            schedule_minstation = minstation_dict.get(key, [])
            schedule_group = group_dict.get(key, [])

            grouped_data[key] = {
                "name": key,
                "schedule_minstation": schedule_minstation,
                "schedule_group": schedule_group
            }

        # Convert the grouped data into a list of objects
        json_data = list(grouped_data.values())

        # Export the JSON data to a file
        with open(outputFile, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

        print(f"Created schedule JSON in {outputFile}")

    except Exception as error:
        print("Error while creating schedule json", error)
