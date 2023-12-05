import sys
from check import dataValid
from formatJsons import format_and_sort_json_files
from consolidateData import consolidateJsons
from createTsBotJson import createTeamspeakStationBotJson
from createScheduleJson import createScheduleJson
from removeRedundant import removeRedundantScheduleEntries

try:
    combinedFile = "data.json"

    folders_to_consolidate = ["edgg", "edmm", "eduu", "edww", "edyy", "edxx"]
    folders_to_sort = folders_to_consolidate + ["event_schedules"]
    dataValid(folders_to_consolidate)

    # remove redundant schedule_groups entries
    removeRedundantScheduleEntries(folders_to_consolidate)

    # format all source jsons
    format_and_sort_json_files(folders_to_sort)

    # consolidate all source files into one combined file
    consolidateJsons(folders_to_consolidate, combinedFile)

    # create schedule json
    createScheduleJson(combinedFile, "legacy/schedule.json")

    # create legacy jsons
    createTeamspeakStationBotJson(combinedFile, "legacy/atc_station_mappings.json")

except Exception as error:
    print(error)
    sys.exit(1)
