import os
import json

def createTeamspeakStationBotJson(inputFile, outputFile):
    try:
        with open(inputFile, 'r') as json_file:
            data = json.load(json_file)
        
        new_data = []

        for item in data:
            # Extract the "frequency" property
            frequency = item.get("frequency", "")
            id = item.get("abbreviation", "")
            
            # Extract the "logon" property and split it by "_"
            logon = item.get("logon", "")
            callsign_parts = logon.split("_")
            callsignPrefix = callsign_parts[0] if callsign_parts else ""

            # Create a new object with the extracted properties
            new_item = {
                "id": id,
                "callsignPrefix": callsignPrefix,
                "frequency": frequency
            }

            new_data.append(new_item)

        # Write the new JSON data to the output file
        with open(outputFile, 'w') as output_json_file:
            json.dump(new_data, output_json_file, indent=2)

        print(f"Created Teamspeak Station Bot JSON in {outputFile}")

    except json.JSONDecodeError as e:
        print(f"Error loading JSON from {inputFile}: {e}")