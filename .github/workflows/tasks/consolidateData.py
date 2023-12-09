import os
import json


def consolidateJsons(folders, outputFile):
    # Initialize an empty list to store combined JSON data
    combined_data = []

    # Function to load and append JSON files from a folder
    def load_and_append_json_files(folder):
        folder_data = []
        for filename in os.listdir(folder):
            if filename.endswith(".json"):
                file_path = os.path.join(folder, filename)
                try:
                    with open(file_path, "r") as json_file:
                        data = json.load(json_file)
                        folder_data.extend(data)  # Use extend to add items to the list
                except json.JSONDecodeError as e:
                    print(f"Error loading JSON from {file_path}: {e}")
        return folder_data

    # Combine JSON data from all folders
    for folder in folders:
        folder_data = load_and_append_json_files(folder)
        combined_data.extend(folder_data)

    combined_data.sort(key=lambda x: (x["logon"]))

    # Write the combined JSON data to a single file
    with open(outputFile, "w") as combined_file:
        json.dump(combined_data, combined_file, indent=2)

    print(f"Combined data from {len(folders)} folders and saved to {outputFile}")
