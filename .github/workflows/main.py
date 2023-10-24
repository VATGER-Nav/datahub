from formatJsons import format_and_sort_json_files
from consolidateData import consolidateJsons
from createTsBotJson import createTeamspeakStationBotJson
from createScheduleJson import createScheduleJson
from removeRedundant import removeRedundantScheduleEntries

combinedFile = "data.json"
folders_to_sort = ['edgg', 'edmm', 'eduu', 'edww', 'edyy', 'event_schedules']
folders_to_consolidate = ['edgg', 'edmm', 'eduu', 'edww', 'edyy']

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

