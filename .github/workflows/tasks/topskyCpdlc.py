import json


def createTopskyCpdlcTxt(input_file, output_file):
    try:
        # Load cpdlc_callsign_map from the file
        with open("topsky/cpdlcMap.json", "r") as callsign_map_file:
            cpdlc_callsign_map = json.load(callsign_map_file)

        # Load data from the inputFile
        with open(input_file, "r") as json_file:
            data = json.load(json_file)

        cpdlc_station_data = []

        for item in data:
            cpdlc_login = item.get("cpdlc_login")
            callsign = cpdlc_callsign_map.get(item.get("logon").split("_")[0])
            abbreviation = item.get("abbreviation")

            if cpdlc_login and callsign and abbreviation:
                cpdlc_station_data.append(
                    {
                        "login": cpdlc_login,
                        "callsign": callsign,
                        "abbreviation": abbreviation,
                    }
                )

        # Sort cpdlc_station_data first by callsign and then by login alphabetically
        sorted_cpdlc_station_data = sorted(
            cpdlc_station_data,
            key=lambda station: (station["callsign"], station["login"]),
        )

        output_lines = []

        # store the last callsign to add line breaks between callsign changes
        last_callsign = None

        for station in sorted_cpdlc_station_data:
            if station["callsign"] != last_callsign:
                # Add an empty line after every change of callsign (excluding the first)
                if last_callsign is not None:
                    output_lines.append("\n")

            output_lines.append(
                f"LOGIN:{station['login']}:{station['callsign']}:{station['abbreviation']}\n"
            )

            last_callsign = station["callsign"]

        with open(output_file, "w") as output_text:
            output_text.writelines(output_lines)

    except Exception as error:
        print("Error while creating cpdlc txt", error)
