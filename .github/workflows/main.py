import sys
from tasks.verifyData import checkData
from tasks.removeRedundantEntries import removeRedundantScheduleEntries
from tasks.formatting import format_and_sort_json_files
from tasks.consolidateData import consolidateJsons
from tasks.tsBotWorkflow import createTeamspeakStationBotJson
from tasks.scheduleWorkflow import createScheduleJson
from tasks.topskyCpdlc import createTopskyCpdlcTxt

try:
    OUTPUT_PATH = "data.json"

    folders_to_consolidate = ["edgg", "edmm", "eduu", "edww", "edyy", "edxx"]
    folders_to_sort = folders_to_consolidate + ["event_schedules"]
    checkData(folders_to_consolidate)

    # remove redundant schedule_groups entries
    removeRedundantScheduleEntries(folders_to_consolidate)

    # format all source jsons
    format_and_sort_json_files(folders_to_sort)

    # consolidate all source files into one combined file
    consolidateJsons(folders_to_consolidate, OUTPUT_PATH)

    # create schedule json
    createScheduleJson(OUTPUT_PATH, "legacy/schedule.json")

    # create legacy jsons
    createTeamspeakStationBotJson(OUTPUT_PATH, "legacy/atc_station_mappings.json")

    # create TopSkyCPDLC.txt
    createTopskyCpdlcTxt(OUTPUT_PATH, "topsky/TopSkyCPDLC.txt")

except Exception as error:
    print(error)
    sys.exit(1)
