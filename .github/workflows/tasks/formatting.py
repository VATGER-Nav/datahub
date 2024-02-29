import os
import json
import sys


def format_and_sort_json_files(folders):
    for folder in folders:
        for filename in os.listdir(folder):
            if filename.endswith('.json'):
                file_path = os.path.join(folder, filename)
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                    # Write the reformatted JSON back to the file
                    with open(file_path, 'w') as json_file:
                        json.dump(data, json_file, indent=2)
                    print(f"Reformatted JSON in {file_path}")
                except json.JSONDecodeError as e:
                    print(f"Error loading JSON from {file_path}: {e}")
                    sys.exit(1)
