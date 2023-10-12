# VATSIM Germany DataHub Repository

Welcome to the VATSIM Germany DataHub Repository! This repository serves as a central storage location for various data related to VATSIM Germany. It is primarily used to support the following projects: Teamspeak Station Bot, Booking System, and ATC Schedule.

## Folder Structure

The repository is organized into the following main folders:

1. **atc_schedules**: This folder contains data used in the ATC schedule project. It includes event schedules and their recurrence patterns (e.g., weekly or bi-weekly) and a list of VATSIM Stations that should be covered for each event.

2. **edgg, edmm, edww, eduu, edyy**: These folders contain data about the individual VATSIM positions of the respective FIR/UIR.

## VATSIM Position Properties

The data stored in each of the ATC position folders is in JSON format and includes the following properties:

| Property            | Description                                                                                                                                                      |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| logon               | VATSIM Logon of the ATC position                                                                                                                                 |
| frequency           | Primary frequency used on VATSIM (required for Teamspeak Station Bot)                                                                                            |
| abbreviation        | Abbreviation (used by the Teamspeak Station Bot)                                                                                                                 |
| description         | Optional description of the ATC position                                                                                                                         |
| schedule_minstation | Specifies on which schedule page the station should always appear, even if not booked                                                                            |
| schedule_groups     | Specifies on which schedule page the station should appear if it is booked on VATBOOK (VATSIM Booking System)                                                    |
| relevant_airports   | Used in the booking system on the VATGER homepage. When the array contains the airport, the station will appear if the airport is selected in the booking system |

## Automated workflows / How to edit data

This repository used github-actions to automatically consolidate and keep consistent formatting.

**The json files in the following folders can be edited:**
edgg, edmm, edww, eduu, edyy, event_schedules

**The following jsons will be updated automatically:**
data.json, atc_station_mappings.json

## Scheduled merges

This repository uses [merge-schedule-action](https://github.com/gr2m/merge-schedule-action) to allow merging on [AIRAC cycles](https://www.nm.eurocontrol.int/RAD/common/airac_dates.html).

In your pull requests, add a line to the end of the pull request description looking like this

```
/schedule 2022-06-08
```

If you need a more precise, timezone-safe setting, you can use an `ISO 8601` date string

```
/schedule 2022-06-08T09:00:00.000Z
```
