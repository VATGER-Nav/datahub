import sys, os, json


def checkData(folders):
    print("Checking data:\n")
    jsonFilesValid = True
    scheduleListsValid = True

    for folder in folders:
        for filename in os.listdir(folder):
            if not filename.endswith(".json"):
                continue

            file_path = os.path.join(folder, filename)

            try:
                with open(file_path, "r") as file:
                    json_content = file.read()
                    data = json.loads(json_content)

                    for element in data:
                        if (
                            not "schedule_minstation" in element
                            and not "schedule_groups" in element
                        ):
                            continue

                        if element.get("schedule_minstation") and not isinstance(
                            element.get("schedule_minstation"), list
                        ):
                            scheduleListsValid = False
                            print(
                                f"Error in {file_path}: {element.get('logon')} schedule_minstation has to be a list"
                            )
                        if element.get("schedule_groups") and not isinstance(
                            element.get("schedule_groups"), list
                        ):
                            scheduleListsValid = False
                            print(
                                f"Error in {file_path}: {element.get('logon')} schedule_groups has to be a list"
                            )

            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {file_path}: {e}")
                jsonFilesValid = False

    if not jsonFilesValid:
        print("Workflow aborted: Jsons are invalid")
        sys.exit(100)
    if not scheduleListsValid:
        print(
            "Workflow aborted: schedule_minstation and schedule_groups must be of type list"
        )
        sys.exit(200)
