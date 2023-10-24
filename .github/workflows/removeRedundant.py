import os, json

def removeRedundantScheduleEntries(folders):
    print("Removing redundant entries: ")
    for folder in folders:
        for filename in os.listdir(folder):
            if not filename.endswith('.json'):
                continue
            file_path = os.path.join(folder, filename)
            try:
                with open(file_path, "r") as json_file:
                    data = json.load(json_file)

                for element in data:
                    if not "schedule_minstation" in element or not "schedule_groups" in element:
                        continue

                    schedule_minstation = element["schedule_minstation"]
                    schedule_group = element["schedule_groups"]

                    # Create a new list for schedule_group without redundant entries
                    new_schedule_group = [group for group in schedule_group if group not in schedule_minstation]

                    if new_schedule_group != schedule_group:
                        print("Removed:", [group for group in schedule_group if group not in new_schedule_group], "from", element["logon"])

                    if not new_schedule_group:
                        del element["schedule_groups"]  # Remove the key if the list is empty
                    else:
                        element["schedule_groups"] = new_schedule_group  # Update with the new list

                with open(file_path, 'w') as json_file:
                    json.dump(data, json_file, indent=2)
            
            except json.JSONDecodeError as e:
                print(f"Error loadig JSON from {file_path}: {e}")

    print("\n\n\n")